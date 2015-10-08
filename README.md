GUI_feature_measure
===================
General user interface designed for measuring features in scientific images.

This interface relies of two files. One of which handles the result of your measurements, contains the class properties. The second, buttons_v3, contains the GUI itself. 

## Buttons file.

To begin you'll need to point the code at your NumPy arrays or .fits files and also define where you're going to save your pickle files.

The program reads in either NumPy arrays or .fits files. Upon running the GUI will appear in a figure window. You will observe that the first image appears with an array of buttons. In order to measure a feature you will need to;
1. Browse through the Images using the forward and backwards buttons. You can either move 1 image at a time or 10 frames at a time.
2. Upon finding a feature to measure, press 'Start Measure', this negins the list where the points will be kept.
..* When you click 'Start Measure', the program remembers the Box you're viewing the feature in (using the python selector tool) and will return to this box later on.
..* Click 'Measure' this initalises the 4 measuring clicks
..* Next we have the length selections. Click the bottom and then the top of the feature. The bottom will remain constant in y but will vary in x as further frames are measured.
..* The viewing box will them zoom in on the width of the feature. A guiding line will appear across the box which is at the mid-point between top and bottom and perpendicular to this line. At this point click to measure the width.
..* Once the second click for the width has been make the viewbox will return to the original one. Click 'Confirm', at this point the 4 clicks and time will be appended to the list.
3. If you make a mistake, click 'Measure' again and you can make the clicks again. Keep an eye on the printed output as this will tell you where you have clicked and which click you're on.
4. You can save multiple features to the same pickle file, when you wish to start measuring a new feature, click 'Start Measure' again.

## Property file
This files contains the property class and functions within it. These fuctions define the properties of your feature, length, width, velocity, inclination from normal and lifetime.

It is designed to interpret the pickle file containg the list produced in measuring the solar features.

You will need to change the arcsecond per pixel value. This should be in the instrument paper for tne images you are using. Currently, the arcsec per pixel is set to that of SDO/AIA of 0.6 arcsec per pixel.

## Using the results

Generally the best way of using these results is in plotting using Matplotlib. You will need a 'import def_prop'.
Calling the routines is as expected, and more likely than not you'll be calling many property files *e.g.*

```python
feats = "a list of your pickle files you've openeed"
max_ls = []
for feat in feature_list:
    max_l = np.max(feat.all_len())
    max_ls.append(max_l)
```

will give you a list of the maximum lengths of your features. NB: you may need a try/exept statement to filter out value errors, depending on how well your measurements went.

If you have any questions, please don't hesitste to get in touch!
