import numpy as np

import sunpy
import sunpy.cm
import astropy.io.fits as pyfits

import pickle

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Cursor

from glob import glob
from def_prop import properties



# input the date i'm looking at
# start at this date
d = '2013_01_24'
prompt = '>'
print "please input the name of the pickle file, remember this is a failsafe in order to not write over recorded data"
sf = raw_input(prompt)



# set up the initial files and some parameter
# change these for each data set
files = glob('/storage2/SDO/jet/*304a*.fits')
files.sort()

# read the fits headers
# used for setting the 
hdulist = pyfits.open('')
prihdr = hdulist[0].header
ondisk = (prihdr['R_SUN'] - 1400)
limb = ondisk

# the plotting instructions
fig = plt.figure()
im = plt.imshow(files[0],origin='lower',interpolation='nearest',vmax=files[0][:,ondisk:].max()/18, vmin=files[0][:,ondisk:].min())
plt.axhline(limb)

# colour map used matching with SDO/AIA 30.4nm 
plt.set_cmap(sunpy.cm.get_cmap('sdoaia304'))
axes = plt.subplot(111)
plt.subplots_adjust(bottom=0.2)


# class using the functions 
prop_list = []
class Index:
    ind = 0
    plot_points = None
    cid = None
    
    def next(self, event):
        self.ind += 1
        i = self.ind % len(files)
        im.set_array(np.load(files[i], mmap_mode='r')[:,:8000])
        my_title.set_text(files[i].replace('/',' ').split()[-1][:-4])
        print 'NEXT'
        try:
            x = np.array(prop_list[-1].points[-1])
            if self.plot_points:
               self.plot_points.set_data(x[:,0],x[:,1])
            else:
                self.plot_points, = axes.plot(x[:,0],x[:,1], "o")
        except:
            pass
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(files)
        im.set_array(np.load(files[i], mmap_mode='r')[:,:8000])
        my_title.set_text(files[i].replace('/',' ').split()[-1][:-4])
        plt.draw()
        
    def begin(self, event):
        print 'START SPICULE'
        prop_list.append(properties(axes.axis(),limb))
        print prop_list[-1]
        self.spic_no = 0
        return

    def fbigskip(self, event):
        self.ind += 9
        self.next(event)
        
    def bbigskip(self, event):
        self.ind -= 9
        self.prev(event)
        
    def points(self, event):
        print 'CONFIRM'
        tempfile = pyfits.open(files[self.ind])
        # you will need to change this depending on 
        # how time is defined in the fits header
        real_time = tempfile['DATE-OBS']

        print len(prop_list[-1].points)
        if len(prop_list[-1].points) > 1:
            try:
                self.abcd[0][1] = prop_list[-1].points[0][0][1]
            except Exception as E:
                print E
                import pdb; pdb.set_trace()
                
        prop_list[-1].addstep(self.ind, real_time, self.abcd[0], self.abcd[1],
                              self.abcd[2], self.abcd[3])
        print prop_list[-1]
    
    def record(self, event):
        print 'RECORD'
        self.abcd = []
        self.cursor = Cursor(axes, useblit=True, color='red', linewidth=1 )
        if self.cid:
            fig.canvas.mpl_disconnect(self.cid)
        self.cid = fig.canvas.mpl_connect('button_press_event', self.get_click)
        
    def get_click(self, event):
        print('you pressed', event.button, event.xdata, event.ydata)
        self.abcd.append([event.xdata, event.ydata])
        print np.shape(self.abcd), len(self.abcd)
        self.check_abcd()
    
    def check_abcd(self):
        if len(self.abcd) == 2:  
            vec_mid = []
            vec_mid.append((self.abcd[0][0] + self.abcd[1][0])/2.0)
            vec_mid.append((self.abcd[0][1] + self.abcd[1][1])/2.0)
            self.midx = vec_mid[0]
            self.midy = vec_mid[1]
            
            c1 = [(self.midx - 20.0), (self.midy - 10.0)]
            c2 = [(self.midx + 20.0), (self.midy + 10.0)]
            axes.axis([c1[0], c2[0], c1[1], c2[1]])
            xran = np.linspace(c1[0], c2[0], 100)
            yran = self.line_equ2(c1, c2)
            self.wid_line = axes.plot(xran, yran)
            return False
            
        elif len(self.abcd) == 4:            
            fig.canvas.mpl_disconnect(self.cid)
            self.cid = None
            del self.cursor
            print self.abcd
            axes.axis(prop_list[-1].BBox)
            self.wid_line[-1].set_visible(False)
            plt.draw()
            return True
        else:
            return False
            
    def save_im(self, event):
        tempfile = pyfits.open(files[self.ind])
        real_time = tempfile['DATE-OBS']        
        print real_time
        # you'll need to change this destiniation to save images of macrospicules
        return plt.savefig('/your_file_path_here/AutoSpic/' + real_time + '.png')
        
    def delete(self, event):
        fig.canvas.mpl_disconnect(self.cid)
        self.cid = None
        try:            
            del self.cursor
        except Exception as E:
            print E
        self.abcd = []
        
    def line_equ1(self, abcd):
        p1 = self.abcd[0]
        p2 = self.abcd[1]
        lin_grad1 = (p2[1] - p1[1])/(p2[0] - p1[0])
        c = p2[1] - lin_grad1*p2[0]
        return lin_grad1, c
        
    def line_equ2(self, c1, c2):
        tb_line = self.line_equ1(self.abcd)
        print "tb line = %f"%tb_line[0]
        lin_grad2 = -1.0/(tb_line[0])
        const = self.midy - self.midx*lin_grad2
        x = np.linspace(c1[0], c2[0], 100)
        y = []
        y = lin_grad2*x + const
        return y

    def zone1(self, event):
        prop_list[-1].zone = "Coronal Hole"
        
    def zone2(self, event):
        prop_list[-1].zone = "Coronal Hole Boundary"

    def zone3(self, event):
        prop_list[-1].zone = "Quiet Sun"        
        
    
        
        

# set up the figure

plt.xlabel('Theta round the centre of the Sun in Radians')
plt.ylabel('Arcseconds')
tempfile = pyfits.open(files[0])
real_time = tempfile['DATE-OBS']
my_title = plt.title('Spicule on the Date of %s' % real_time)


# create some buttons
callback = Index()
axskip = plt.axes([0.81, 0.05, 0.1, 0.075])
axbskip = plt.axes([0.81, 0.15, 0.1, 0.075])
axnext = plt.axes([0.7, 0.05, 0.1, 0.075])
axprev = plt.axes([0.59, 0.05, 0.1, 0.075])
axmeas = plt.axes([0.48, 0.05, 0.1, 0.075])
axrec = plt.axes([0.37, 0.05, 0.1, 0.075])
axstart = plt.axes([0.26, 0.05, 0.1, 0.075])
axsave = plt.axes([0.15, 0.05, 0.1, 0.075])
axdel = plt.axes([0.04, 0.05, 0.1, 0.075])
axzone1 = plt.axes([0.04, 0.15, 0.1, 0.075])
axzone2 = plt.axes([0.15, 0.15, 0.1, 0.075])
axzone3 = plt.axes([0.26, 0.15, 0.1, 0.075])


bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)

bskip = Button(axskip, 'Skip >')
bskip.on_clicked(callback.fbigskip)

bbskip = Button(axbskip, 'Skip <')
bbskip.on_clicked(callback.bbigskip)

bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

bstart = Button(axstart, 'Start Spicule')
bstart.on_clicked(callback.begin)

bmeas = Button(axmeas, 'Confirm')
bmeas.on_clicked(callback.points)

brec = Button(axrec, 'Measure')
brec.on_clicked(callback.record)

bsave = Button(axsave, 'Save Image')
bsave.on_clicked(callback.save_im)

bdelete = Button(axdel, 'Delete')
bdelete.on_clicked(callback.delete)

bposs = Button(axzone1, "Coronal Hole.")
bposs.on_clicked(callback.zone1)

bposs1 = Button(axzone2, "C. H. Boundary.")
bposs1.on_clicked(callback.zone2)

bposs2 = Button(axzone3, "Quiet Sun")
bposs2.on_clicked(callback.zone3)

plt.show()



# save the spicule
# define the file path to save the pickle files out to
f = open("/home/sam/Dropbox/Sam/test/" + sf + ".pik",'wb')
pickle.dump(prop_list,f)
f.close()

print 'Im finished now!'
