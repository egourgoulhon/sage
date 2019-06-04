# -*- coding: utf-8 -*-
"""
    multi documentation in Sphinx
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The goal of this extension is to manage a multi documentation in Sphinx.
    To be able to compile Sage's huge documentation in parallel, the
    documentation is cut into a bunch of independent documentations called
    "subdocs", which are compiled separately. There is a master document which
    points to all the subdocs. The intersphinx extension ensures that the
    cross-link between the subdocs are correctly resolved. However some work
    is needed to build a global index. This is the goal of multidocs.

    More precisely this extension ensures the correct merging of
    - the todo list if this extension is activated;
    - the python indexes;
    - the list of python modules;
    - the javascript index;
    - the citations.
"""
import six
from six.moves import cPickle
from six import text_type

import os
import sys
import shutil
import re
import tempfile
import sphinx
from sphinx.util.console import bold
from sage.env import SAGE_DOC
from sage.misc.misc import sage_makedirs

logger = sphinx.util.logging.getLogger(__name__)

CITE_FILENAME = 'citations.pickle'


def merge_environment(app, env):
    """
    Merges the following attributes of the sub-docs environment into the main
    environment:
    - titles                      # Titles
    - todo_all_todos              # ToDo's
    - indexentries                # global python index
    - all_docs                    # needed by the js index
    - citations                   # citations

    - domaindata['py']['modules'] # list of python modules
    """
    logger.info(bold('Merging environment/index files...'))
    for curdoc in app.env.config.multidocs_subdoc_list:
        logger.info("    %s:"%curdoc, nonl=1)
        docenv = get_env(app, curdoc)
        if docenv is not None:
            fixpath = lambda path: os.path.join(curdoc, path)
            logger.info(" %s todos, %s index, %s citations"%(
                    len(docenv.todo_all_todos),
                    len(docenv.indexentries),
                    len(docenv.domaindata["std"]["citations"])
                    ), nonl=1)

            # merge titles
            for t in docenv.titles:
                env.titles[fixpath(t)] = docenv.titles[t]
            # merge the todo links
            for dct in docenv.todo_all_todos:
                dct['docname'] = fixpath(dct['docname'])
            env.todo_all_todos += docenv.todo_all_todos
            # merge the html index links
            newindex = {}
            for ind in docenv.indexentries:
                if ind.startswith('sage/'):
                    newindex[fixpath(ind)] = docenv.indexentries[ind]
                else:
                    newindex[ind] = docenv.indexentries[ind]
            env.indexentries.update(newindex)
            # merge the all_docs links, needed by the js index
            newalldoc = {}
            for ind in docenv.all_docs:
                newalldoc[fixpath(ind)] = docenv.all_docs[ind]
            env.all_docs.update(newalldoc)
            # needed by env.check_consistency (sphinx.environement, line 1734)
            for ind in newalldoc:
                # treat subdocument source as orphaned file and don't complain
                md = env.metadata.get(ind, dict())
                md['orphan'] = 1
                env.metadata[ind] = md
            # merge the citations
            newcite = {}
            citations = docenv.domaindata["std"]["citations"]
            for ind, (path, tag, lineno) in six.iteritems(docenv.domaindata["std"]["citations"]):
                # TODO: Warn on conflicts
                newcite[ind] = (fixpath(path), tag, lineno)
            env.domaindata["std"]["citations"].update(newcite)
            # merge the py:module indexes
            newmodules = {}
            for ind,(modpath,v1,v2,v3) in (
                six.iteritems(docenv.domaindata['py']['modules'])):
                newmodules[ind] = (fixpath(modpath),v1,v2,v3)
            env.domaindata['py']['modules'].update(newmodules)
            logger.info(", %s modules"%(len(newmodules)))
    logger.info('... done (%s todos, %s index, %s citations, %s modules)'%(
            len(env.todo_all_todos),
            len(env.indexentries),
            len(env.domaindata["std"]["citations"]),
            len(env.domaindata['py']['modules'])))
    write_citations(app, env.domaindata["std"]["citations"])


def get_env(app, curdoc):
    """
    Get the environment of a sub-doc from the pickle
    """
    from sphinx.application import ENV_PICKLE_FILENAME
    filename = os.path.join(
        app.env.doctreedir, curdoc, ENV_PICKLE_FILENAME)
    try:
        f = open(filename, 'rb')
    except IOError:
        logger.info("")
        logger.warning("Unable to fetch %s " % filename)
        return None
    docenv = cPickle.load(f)
    f.close()
    return docenv


def merge_js_index(app):
    """
    Merge the JS indexes of the sub-docs into the main JS index
    """
    logger.info('')
    logger.info(bold('Merging js index files...'))
    mapping = app.builder.indexer._mapping
    for curdoc in app.env.config.multidocs_subdoc_list:
        logger.info("    %s:"%curdoc, nonl=1)
        fixpath = lambda path: os.path.join(curdoc, path)
        index = get_js_index(app, curdoc)
        if index is not None:
            # merge the mappings
            logger.info(" %s js index entries"%(len(index._mapping)))
            for (ref, locs) in six.iteritems(index._mapping):
                newmapping = set(map(fixpath, locs))
                if ref in mapping:
                    newmapping = mapping[ref] | newmapping
                mapping[text_type(ref)] = newmapping
            # merge the titles
            titles = app.builder.indexer._titles
            for (res, title) in six.iteritems(index._titles):
                titles[fixpath(res)] = title
            # merge the filenames
            filenames = app.builder.indexer._filenames
            for (res, filename) in six.iteritems(index._filenames):
                filenames[fixpath(res)] = fixpath(filename)
            # TODO: merge indexer._objtypes, indexer._objnames as well

            # Setup source symbolic links
            dest = os.path.join(app.outdir, "_sources", curdoc)
            if not os.path.exists(dest):
                os.symlink(os.path.join("..", curdoc, "_sources"), dest)
    logger.info('... done (%s js index entries)'%(len(mapping)))
    logger.info(bold('Writing js search indexes...'), nonl=1)
    return [] # no extra page to setup


def get_js_index(app, curdoc):
    """
    Get the JS index of a sub-doc from the file
    """
    from sphinx.search import IndexBuilder, languages
    # FIXME: find the correct lang
    sphinx_version=__import__("sphinx").__version__
    if (sphinx_version < '1.2'):
        indexer = IndexBuilder(app.env, 'en',
                               app.config.html_search_options)
    else:
        indexer = IndexBuilder(app.env, 'en',
                               app.config.html_search_options, scoring=None)
    indexfile = os.path.join(app.outdir, curdoc, 'searchindex.js')
    try:
        f = open(indexfile, 'r')
    except IOError:
        logger.info("")
        logger.warning("Unable to fetch %s " % indexfile)
        return None
    indexer.load(f, sphinx.search.js_index)
    f.close()
    return indexer


mustbefixed = ['search', 'genindex', 'genindex-all',
               'py-modindex', 'searchindex.js']


def fix_path_html(app, pagename, templatename, ctx, event_arg):
    """
    Fixes the context so that the files
    - search.html
    - genindex.html
    - py-modindex.html
    point to the right place, that is in
        reference/
    instead of
        reference/subdocument
    """
    # sphinx/builder/html.py line 702
    # def pathto(otheruri, resource=False,
    #            baseuri=self.get_target_uri(pagename)):
    old_pathto = ctx['pathto']
    def sage_pathto(otheruri, *args, **opts):
        if otheruri in mustbefixed:
            otheruri = os.path.join("..", otheruri)
        return old_pathto(otheruri, *args, **opts)
    ctx['pathto'] = sage_pathto


def citation_dir(app):
    # Split app.outdir in 3 parts: SAGE_DOC/TYPE/TAIL where TYPE
    # is a single directory and TAIL can contain multiple directories.
    # The citation dir is then SAGE_DOC/inventory/TAIL.
    assert app.outdir.startswith(SAGE_DOC)
    rel = app.outdir[len(SAGE_DOC):]
    dirs = rel.split(os.sep)
    # If SAGE_DOC does not end with a slash, rel will start with
    # a slash giving an empty dirs[0]. Remove this:
    if not dirs[0]:
        dirs.pop(0)
    dirs = [SAGE_DOC, "inventory"] + dirs[1:]
    citedir = os.path.join(*dirs)
    sage_makedirs(citedir)
    return citedir


def write_citations(app, citations):
    """
    Pickle the citation in a file.
    """
    from sage.misc.temporary_file import atomic_write
    outdir = citation_dir(app)
    with atomic_write(os.path.join(outdir, CITE_FILENAME), binary=True) as f:
        cPickle.dump(citations, f)
    logger.info("Saved pickle file: %s" % CITE_FILENAME)


def fetch_citation(app, env):
    """
    Fetch the global citation index from the refman to allow for cross
    references.
    """
    logger.info(bold('loading cross citations... '), nonl=1)
    filename = os.path.join(citation_dir(app), '..', CITE_FILENAME)
    if not os.path.isfile(filename):
        return
    with open(filename, 'rb') as f:
        cache = cPickle.load(f)
    logger.info("done (%s citations)."%len(cache))
    cite = env.domaindata["std"]["citations"]
    for ind, (path, tag, lineno) in six.iteritems(cache):
        if ind not in cite: # don't override local citation
            cite[ind] = (os.path.join("..", path), tag, lineno)


def init_subdoc(app):
    """
    Init the merger depending on if we are compiling a subdoc or the master
    doc itself.
    """
    if app.config.multidocs_is_master:
        logger.info(bold("Compiling the master document"))
        app.connect('env-updated', merge_environment)
        app.connect('html-collect-pages', merge_js_index)
        if app.config.multidocs_subdoc_list:
            # Master file with indexes computed by merging indexes:
            # Monkey patch index fetching to silence warning about broken index
            def load_indexer(docnames):
                logger.info(bold('skipping loading of indexes... '), nonl=1)
            app.builder.load_indexer = load_indexer

    else:
        logger.info(bold("Compiling a sub-document"))
        app.connect('html-page-context', fix_path_html)
        if not app.config.multidoc_first_pass:
            app.connect('env-updated', fetch_citation)

        # Monkey patch copy_static_files to make a symlink to "../"
        def link_static_files():
            """
            Instead of copying static files, make a link to the master static file.
            See sphinx/builder/html.py line 536::

                class StandaloneHTMLBuilder(Builder):
                [...]
                    def copy_static_files(self):
                    [...]
            """
            logger.info(bold('linking _static directory.'))
            static_dir = os.path.join(app.builder.outdir, '_static')
            master_static_dir = os.path.join('..', '_static')
            if os.path.lexists(static_dir):
                try:
                    shutil.rmtree(static_dir)
                except OSError:
                    os.unlink(static_dir)
            os.symlink(master_static_dir, static_dir)

        app.builder.copy_static_files = link_static_files

    if app.config.multidoc_first_pass == 1:
        app.config.intersphinx_mapping = {}
    else:
        app.emit('env-check-consistency', app.env)



def setup(app):
    app.add_config_value('multidocs_is_master', True, True)
    app.add_config_value('multidocs_subdoc_list', [], True)
    app.add_config_value('multidoc_first_pass', 0, False)   # 1 = deactivate the loading of the inventory
    app.connect('builder-inited', init_subdoc)
