# Anomalies detection in asphalt pavements

Ordinary Test: Computer Visiin V6 - JAN-JUN 2015 - FIME - UANL

## Description

- Get the image to process in <i>/input</i> folder
- Pre-processing the image with filters for found the road segmented
- Segmented road with original pixels in background
- Finding foreground area for anomalies in road
- Subtract anomalies shapes from background
- Image Segmentation with Watershed Algorithm (OpenCV)
- Find anomalies contours for display results in console
- Display anomalies in asphalt pavement found.
- Shows if necessary repair the road.

## Libraries

- Python 2.7+
- OpenCV > 2.4.2
- NumPy, Pygame y PIL instaladas

# Test

![Alt text](https://github.com/chrismedrdz/Computer-Vision/blob/master/1488028/capture.PNG "Test in Windows")


## For Extra points
It is proposed that the city has various specialized agency depending size, where recive anomalies in asphalt reports automatically. Pavement surface images will be collected through automated means by diverse agencies, whereas automated processing of pavement surface is executed only some by those agencies.
<BR/>
I propose for collect images automatically, placing various sensors at traffic lights, where you capture the image of the pavement by a camera with good resolution if a car suffers a abrupt  movement, ie, has passed above a anomalie. The capture will be shot when the car has moved.
<BR/>
This collected images will be send to city agencies from process and determien if its necessary repair the road in this zone. For best performance, it is suggested implemented a distributed system so that before it send image of the possible anomaly, some servers really validate the real asphalt failures before sending to agencies.

## References

+ <b>Image Segmentation with Watershed Algorithm</b>
  - <i>http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_watershed/py_watershed.html</i>

+ <b>A Morphological Image Processing Approach</b>
  - <i>http://www.upf.br/seer/index.php/rbca/article/download/3661/2549</i>

+ <b>Automated Pavement Distress Collection Techniques</b>
  - <i>http://onlinepubs.trb.org/onlinepubs/nchrp/nchrp_syn_334.pdf</i>

## Autor

Christopher Medina Rodríguez - 1488028
email: chris.medrdz@gmail.com