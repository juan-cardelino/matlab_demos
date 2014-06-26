"""
demo example for the X->aX+b transform
"""

from lib import base_app, build, http, image
from lib.misc import app_expose, ctime
from lib.base_app import init_app
import cherrypy
from cherrypy import TimeoutError
import os.path
import shutil

class app(base_app):
    """ matlab sobel demo """
    
    title = "matlab sobel demo"
    xlink_article = 'http://www.ipol.im/'

    input_nb = 1 # number of input images
    input_max_pixels = 50000000 # max size (in pixels) of an input image
    input_max_weight = 1 * 4024 * 4024 # max size (in bytes) of an input file
    input_dtype = '1x8i' # input image expected data type
    input_ext = '.pgm'   # input image expected extension (ie file format)
    is_test = True       # switch to False for deployment
    is_visible = True
    is_listed = True



    def __init__(self):
        """
        app setup
        """
        # setup the parent class
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_app.__init__(self, base_dir)

        # select the base_app steps to expose
        # index() is generic
        app_expose(base_app.index)
        app_expose(base_app.input_select)
        app_expose(base_app.input_upload)
        # params() is modified from the template
        app_expose(base_app.params)
        # run() and result() must be defined here

    def build(self):
        """
        program build/update
        """
        # store common file path in variables
        tgz_file = self.dl_dir + "matlab_sobel.zip"
        prog_file = self.bin_dir + "matrixdriver"
        prog_file2 = self.bin_dir + "run_algo.sh"
        prog_file3 = self.bin_dir + "libmatrixp.so"
        log_file = self.base_dir + "build.log"
        # get the latest source archive
        build.download("http://dev.ipol.im/~juanc/matlab_sobel.zip" , tgz_file)
        # test if the dest file is missing, or too old
        if (os.path.isfile(prog_file)
            and ctime(tgz_file) < ctime(prog_file)):
            cherrypy.log("not rebuild needed",
                         context='BUILD', traceback=False)
        else:
            # extract the archive
            build.extract(tgz_file, self.src_dir)
            # build the program
            build.run("make -j4 -C %s " % (self.src_dir + "matlab_sobel"), stdout=log_file)
            # save into bin dir
            if os.path.isdir(self.bin_dir):
                shutil.rmtree(self.bin_dir)
            os.mkdir(self.bin_dir)
            shutil.copy(self.src_dir + os.path.join("matlab_sobel", "out",
                                                    "matrixdriver"), prog_file)
            shutil.copy(self.src_dir + os.path.join("matlab_sobel", 
                                                    "run_algo.sh"), prog_file2)
            shutil.os.chmod(prog_file2, 0775)
            shutil.os.chmod(prog_file, 0775)
            shutil.copy(self.src_dir + os.path.join("matlab_sobel", "lib",
                                                    "libmatrixp.so"), prog_file3)
            # cleanup the source dir
            shutil.rmtree(self.src_dir)
        return

    @cherrypy.expose
    @init_app
    def wait(self, a="1.", b="0"):
        """
        params handling and run redirection
        """
        # save and validate the parameters
        try:
            self.cfg['param'] = {'a' : float(a),
                                 'b' : float(b)}
            self.cfg.save()
        except ValueError:
            return self.error(errcode='badparams',
                              errmsg="The parameters must be numeric.")

        http.refresh(self.base_url + 'run?key=%s' % self.key)
        return self.tmpl_out("wait.html")

    @cherrypy.expose
    @init_app
    def run(self):
        """
        algo execution
        """
        # read the parameters
        a = self.cfg['param']['a']
        b = self.cfg['param']['b']
        # run the algorithm
        try:
            self.run_algo(a, b)
        except TimeoutError:
            return self.error(errcode='timeout') 
        except RuntimeError:
            return self.error(errcode='runtime')
        http.redir_303(self.base_url + 'result?key=%s' % self.key)

        # archive
        if self.cfg['meta']['original']:
            ar = self.make_archive()
            ar.add_file("input_0.orig.png", "original.png", info="uploaded")
            ar.add_file("input_0.png", "input.png", info="input")
            ar.add_file("output.png", info="output")
            ar.add_info({"a": a, "b": b})
            ar.save()

        return self.tmpl_out("run.html")

    def run_algo(self, a, b):
        """
        the core algo runner
        could also be called by a batch processor
        this one needs no parameter
        """
        p = self.run_proc(['run_algo.sh', 'input_0.png', 'output.png']) #, self.bin_dir])
        self.wait_proc(p, timeout=self.timeout)
        return

    @cherrypy.expose
    @init_app
    def result(self):
        """
        display the algo results
        """
        return self.tmpl_out("result.html",
                             height=image(self.work_dir
                                          + 'output.png').size[1])
