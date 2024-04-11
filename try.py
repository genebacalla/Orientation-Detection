from orientation import OrientationDetection
from imutils.paths import list_images
import cv2

load_directory = 'bottles'
save_directory = 'oriented'
bbox = OrientationDetection()

ctr=0
for images in list_images(load_directory):
    print(images)
    image = cv2.imread(images)
    out_image = bbox.testOrientation(image)

    img_name = f"image_{ctr}"
    cv2.imwrite(f"{save_directory}/{img_name}.jpg", out_image)
    # cv2.imshow('hehe', bbox.cropbbox)
    ctr+=1
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
