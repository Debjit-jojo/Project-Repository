"""Backend logic for Image Processing Lab."""

import base64
import cv2
import numpy as np

# PRACTICAL / POST LAB DATA
# ============================================================

PRACTICALS = [
    {
        "id": "p02",
        "title": "Practical 02",
        "subtitle": "Image Arithmetic & Bitwise Operations",
        "operations": [
            ("rgb", "RGB Image"),
            ("gray", "Grayscale"),
            ("binary", "Binary"),
            ("addition", "Image Addition"),
            ("subtraction", "Image Subtraction"),
            ("multiplication", "Image Multiplication"),
            ("bitwise_and", "Bitwise AND"),
            ("bitwise_or", "Bitwise OR"),
            ("bitwise_xor", "Bitwise XOR"),
            ("bitwise_not", "Bitwise NOT")
        ]
    },
    {
        "id": "p03",
        "title": "Practical 03",
        "subtitle": "Geometric Transformations",
        "operations": [
            ("translation", "Translation"),
            ("rotation", "Rotation"),
            ("scaling", "Scaling"),
            ("shear_x", "X Shearing"),
            ("shear_y", "Y Shearing"),
            ("reflect_x", "X Reflection"),
            ("reflect_y", "Y Reflection"),
            ("crop", "Cropping")
        ]
    },
    {
        "id": "p04",
        "title": "Practical 04",
        "subtitle": "Image Enhancement & Thresholding",
        "operations": [
            ("negative", "Negative"),
            ("brightness", "Brightness & Contrast"),
            ("laplacian", "Laplacian Sharpening"),
            ("histogram", "Histogram Equalization"),
            ("threshold_binary", "Binary Threshold"),
            ("threshold_inverse", "Inverse Threshold"),
            ("threshold_trunc", "Truncate Threshold"),
            ("threshold_zero", "To Zero Threshold"),
            ("threshold_zi", "To Zero Inverted")
        ]
    },
    {
        "id": "p05",
        "title": "Practical 05",
        "subtitle": "Image Filtering",
        "operations": [
            ("average", "Averaging Filter"),
            ("gaussian", "Gaussian Filter"),
            ("median", "Median Filter"),
            ("bilateral", "Bilateral Filter")
        ]
    },
    {
        "id": "p06",
        "title": "Practical 06",
        "subtitle": "Noise Removal & Inpainting",
        "operations": [
            ("gaussian_noise", "Gaussian Noise Removal"),
            ("sp_noise", "Salt & Pepper Removal"),
            ("nlm", "Non-Local Means"),
            ("telea", "Telea Inpainting"),
            ("ns", "Navier-Stokes Inpainting")
        ]
    },
    {
        "id": "p07",
        "title": "Practical 07",
        "subtitle": "Image Compression",
        "operations": [
            ("jpeg", "JPEG Compression"),
            ("png", "PNG Compression"),
            ("rle", "Run Length Encoding"),
            ("lzw", "LZW Compression")
        ]
    },
    {
        "id": "p08",
        "title": "Practical 08",
        "subtitle": "Binary Morphological Operations",
        "operations": [
            ("erosion", "Erosion"),
            ("dilation", "Dilation"),
            ("opening", "Opening"),
            ("closing", "Closing")
        ]
    },
    {
        "id": "p09",
        "title": "Practical 09",
        "subtitle": "Correlation & Template Matching",
        "operations": [
            ("correlation", "Correlation / Template Matching")
        ]
    }
]

POST_LABS = [
    ("post_hsv", "HSV Color Space"),
    ("post_ycrcb", "YCrCb Color Space"),
    ("post_lab", "Lab Color Space"),
    ("post_canny", "Canny Edge Detection"),
    ("post_sobel", "Sobel Edge Detection"),
    ("post_prewitt", "Prewitt Edge Detection")
]


OP_INFO = {
    "rgb": "Converts and displays the image in RGB representation.",
    "gray": "Converts the input image from BGR/RGB representation into grayscale.",
    "binary": "Creates a binary image using a threshold value.",
    "addition": "Adds two images pixel by pixel.",
    "subtraction": "Subtracts the second image from the first image.",
    "multiplication": "Performs pixel-wise image multiplication.",
    "bitwise_and": "Performs logical AND operation between two images.",
    "bitwise_or": "Performs logical OR operation between two images.",
    "bitwise_xor": "Performs logical XOR operation between two images.",
    "bitwise_not": "Inverts the binary values of the input image.",
    "translation": "Moves the image horizontally and vertically.",
    "rotation": "Rotates the image around its center.",
    "scaling": "Changes the size of the image.",
    "shear_x": "Applies horizontal shearing.",
    "shear_y": "Applies vertical shearing.",
    "reflect_x": "Reflects the image around the X-axis.",
    "reflect_y": "Reflects the image around the Y-axis.",
    "crop": "Extracts the central portion of the image.",
    "negative": "Creates the photographic negative of the image.",
    "brightness": "Changes image brightness and contrast.",
    "laplacian": "Uses Laplacian filtering for image sharpening.",
    "histogram": "Improves contrast using histogram equalization.",
    "threshold_binary": "Applies binary thresholding.",
    "threshold_inverse": "Applies inverse binary thresholding.",
    "threshold_trunc": "Applies truncation thresholding.",
    "threshold_zero": "Applies To Zero thresholding.",
    "threshold_zi": "Applies To Zero Inverted thresholding.",
    "average": "Smooths the image using an averaging filter.",
    "gaussian": "Reduces noise using Gaussian smoothing.",
    "median": "Reduces impulse noise using median filtering.",
    "bilateral": "Smooths the image while preserving edges.",
    "gaussian_noise": "Reduces Gaussian noise using Gaussian filtering.",
    "sp_noise": "Reduces salt-and-pepper noise using median filtering.",
    "nlm": "Uses Non-Local Means denoising.",
    "telea": "Performs image inpainting using the Telea method.",
    "ns": "Performs image inpainting using the Navier-Stokes method.",
    "jpeg": "Compresses the image using JPEG encoding.",
    "png": "Compresses the image using PNG encoding.",
    "rle": "Calculates an educational Run Length Encoding estimate.",
    "lzw": "Calculates an educational LZW compression estimate.",
    "erosion": "Shrinks foreground regions using erosion.",
    "dilation": "Expands foreground regions using dilation.",
    "opening": "Performs erosion followed by dilation.",
    "closing": "Performs dilation followed by erosion.",
    "correlation": "Performs template matching using normalized correlation.",
    "post_hsv": "Converts the image to HSV and reconstructs it for display.",
    "post_ycrcb": "Converts the image to YCrCb and reconstructs it for display.",
    "post_lab": "Converts the image to Lab and reconstructs it for display.",
    "post_canny": "Detects edges using the Canny edge detector.",
    "post_sobel": "Detects edges using Sobel operators.",
    "post_prewitt": "Detects edges using Prewitt operators."
}


# ============================================================
# IMAGE HELPERS
# ============================================================

def read_uploaded_image(file):
    if file is None or file.filename == "":
        raise ValueError("Please upload an image.")

    data = file.read()

    if not data:
        raise ValueError("The uploaded file is empty.")

    array = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Unable to read the uploaded image.")

    return image


def resize_second_image(image1, image2):
    h, w = image1.shape[:2]
    return cv2.resize(image2, (w, h))


def image_to_base64(image):
    if image is None:
        return None

    if len(image.shape) == 2:
        output = image
    else:
        output = image

    output = np.clip(output, 0, 255).astype(np.uint8)

    success, buffer = cv2.imencode(".png", output)

    if not success:
        return None

    return base64.b64encode(buffer).decode("utf-8")


def calculate_statistics(image):
    if image is None:
        return {}

    height, width = image.shape[:2]

    if len(image.shape) == 2:
        channels = 1
    else:
        channels = image.shape[2]

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "pixels": width * height,
        "dtype": str(image.dtype),
        "minimum": int(np.min(image)),
        "maximum": int(np.max(image)),
        "mean": round(float(np.mean(image)), 2)
    }


def create_mask(image):
    """
    Creates a small central mask for demonstration of
    automatic inpainting.
    """
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    h, w = mask.shape

    box_w = max(10, int(w * 0.12))
    box_h = max(10, int(h * 0.12))

    x1 = max(0, w // 2 - box_w // 2)
    y1 = max(0, h // 2 - box_h // 2)

    x2 = min(w, x1 + box_w)
    y2 = min(h, y1 + box_h)

    mask[y1:y2, x1:x2] = 255

    return mask


# ============================================================
# COMPRESSION ESTIMATES
# ============================================================

def rle_estimate(image):
    """
    Educational RLE estimate.
    The image is reduced before calculation to keep
    processing fast.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape

    scale = min(1.0, 256 / max(h, w))

    if scale < 1.0:
        gray = cv2.resize(
            gray,
            (
                max(1, int(w * scale)),
                max(1, int(h * scale))
            )
        )

    data = gray.flatten()

    if len(data) == 0:
        return 0, 0

    runs = 1 + int(np.count_nonzero(data[1:] != data[:-1]))

    original = len(data)

    estimated = runs * 2

    return original, estimated


def lzw_estimate(image):
    """
    Educational LZW estimate.
    Only a limited grayscale sample is used so that
    the browser application remains responsive.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape

    scale = min(1.0, 256 / max(h, w))

    if scale < 1.0:
        gray = cv2.resize(
            gray,
            (
                max(1, int(w * scale)),
                max(1, int(h * scale))
            )
        )

    data = gray.flatten().tolist()

    data = data[:65536]

    if not data:
        return 0, 0

    dictionary = {bytes([i]): i for i in range(256)}

    next_code = 256
    current = bytes([data[0]])
    codes = 0

    for value in data[1:]:
        symbol = bytes([value])
        combined = current + symbol

        if combined in dictionary:
            current = combined
        else:
            codes += 1

            if next_code < 65535:
                dictionary[combined] = next_code
                next_code += 1

            current = symbol

    codes += 1

    return len(data), codes


# ============================================================
# IMAGE PROCESSING ENGINE
# ============================================================

def process_image(image, operation, form, second_image=None):

    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    if operation == "rgb":
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), "RGB representation generated."

    # --------------------------------------------------------
    # GRAYSCALE
    # --------------------------------------------------------

    if operation == "gray":
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return result, "Grayscale image generated."

    # --------------------------------------------------------
    # BINARY
    # --------------------------------------------------------

    if operation == "binary":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold = int(form.get("threshold", 127))
        threshold = max(0, min(255, threshold))

        _, result = cv2.threshold(
            gray,
            threshold,
            255,
            cv2.THRESH_BINARY
        )

        return result, f"Binary threshold applied at {threshold}."

    # --------------------------------------------------------
    # TWO IMAGE OPERATIONS
    # --------------------------------------------------------

    if operation in [
        "addition",
        "subtraction",
        "multiplication",
        "bitwise_and",
        "bitwise_or",
        "bitwise_xor"
    ]:

        if second_image is None:
            raise ValueError(
                "This operation requires a second image."
            )

        second_image = resize_second_image(image, second_image)

        if operation == "addition":
            result = cv2.add(image, second_image)
            return result, "Two images added pixel by pixel."

        if operation == "subtraction":
            result = cv2.subtract(image, second_image)
            return result, "Second image subtracted from first image."

        if operation == "multiplication":
            a = image.astype(np.float32) / 255.0
            b = second_image.astype(np.float32) / 255.0

            result = np.clip(a * b * 255, 0, 255).astype(np.uint8)

            return result, "Two images multiplied pixel by pixel."

        if operation == "bitwise_and":
            result = cv2.bitwise_and(image, second_image)
            return result, "Bitwise AND operation completed."

        if operation == "bitwise_or":
            result = cv2.bitwise_or(image, second_image)
            return result, "Bitwise OR operation completed."

        if operation == "bitwise_xor":
            result = cv2.bitwise_xor(image, second_image)
            return result, "Bitwise XOR operation completed."

    # --------------------------------------------------------
    # BITWISE NOT
    # --------------------------------------------------------

    if operation == "bitwise_not":
        result = cv2.bitwise_not(image)
        return result, "Bitwise NOT operation completed."

    # --------------------------------------------------------
    # TRANSLATION
    # --------------------------------------------------------

    if operation == "translation":

        x = int(float(form.get("tx", 100)))
        y = int(float(form.get("ty", 50)))

        matrix = np.float32([
            [1, 0, x],
            [0, 1, y]
        ])

        h, w = image.shape[:2]

        result = cv2.warpAffine(
            image,
            matrix,
            (w, h)
        )

        return result, f"Translated by X={x}, Y={y}."

    # --------------------------------------------------------
    # ROTATION
    # --------------------------------------------------------

    if operation == "rotation":

        angle = float(form.get("angle", 30))

        h, w = image.shape[:2]

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        result = cv2.warpAffine(
            image,
            matrix,
            (w, h)
        )

        return result, f"Image rotated by {angle} degrees."

    # --------------------------------------------------------
    # SCALING
    # --------------------------------------------------------

    if operation == "scaling":

        scale = float(form.get("scale", 0.6))

        scale = max(0.1, min(3.0, scale))

        result = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_LINEAR
        )

        return result, f"Image scaled by factor {scale}."

    # --------------------------------------------------------
    # X SHEARING
    # --------------------------------------------------------

    if operation == "shear_x":

        shear = float(form.get("shear", 0.3))

        h, w = image.shape[:2]

        matrix = np.float32([
            [1, shear, 0],
            [0, 1, 0]
        ])

        new_width = int(w + abs(shear) * h)

        result = cv2.warpAffine(
            image,
            matrix,
            (new_width, h)
        )

        return result, f"X shearing applied with factor {shear}."

    # --------------------------------------------------------
    # Y SHEARING
    # --------------------------------------------------------

    if operation == "shear_y":

        shear = float(form.get("shear", 0.3))

        h, w = image.shape[:2]

        matrix = np.float32([
            [1, 0, 0],
            [shear, 1, 0]
        ])

        new_height = int(h + abs(shear) * w)

        result = cv2.warpAffine(
            image,
            matrix,
            (w, new_height)
        )

        return result, f"Y shearing applied with factor {shear}."

    # --------------------------------------------------------
    # REFLECTION
    # --------------------------------------------------------

    if operation == "reflect_x":

        result = cv2.flip(image, 0)

        return result, "X-axis reflection completed."

    if operation == "reflect_y":

        result = cv2.flip(image, 1)

        return result, "Y-axis reflection completed."

    # --------------------------------------------------------
    # CROPPING
    # --------------------------------------------------------

    if operation == "crop":

        h, w = image.shape[:2]

        x1 = int(w * 0.20)
        x2 = int(w * 0.80)

        y1 = int(h * 0.20)
        y2 = int(h * 0.80)

        result = image[y1:y2, x1:x2]

        return result, "Central 60% of the image cropped."

    # --------------------------------------------------------
    # NEGATIVE
    # --------------------------------------------------------

    if operation == "negative":

        result = 255 - image

        return result, "Image negative generated."

    # --------------------------------------------------------
    # BRIGHTNESS & CONTRAST
    # --------------------------------------------------------

    if operation == "brightness":

        alpha = float(form.get("alpha", 2.3))
        beta = int(float(form.get("beta", 10)))

        alpha = max(0.1, min(5.0, alpha))
        beta = max(-255, min(255, beta))

        result = cv2.convertScaleAbs(
            image,
            alpha=alpha,
            beta=beta
        )

        return result, f"Contrast={alpha}, Brightness={beta}."

    # --------------------------------------------------------
    # LAPLACIAN SHARPENING
    # --------------------------------------------------------

    if operation == "laplacian":

        lap = cv2.Laplacian(
            image,
            cv2.CV_64F
        )

        lap = np.uint8(
            np.absolute(lap)
        )

        result = cv2.addWeighted(
            image,
            1.0,
            lap,
            1.0,
            0
        )

        return result, "Laplacian sharpening completed."

    # --------------------------------------------------------
    # HISTOGRAM EQUALIZATION
    # --------------------------------------------------------

    if operation == "histogram":

        if len(image.shape) == 3:

            ycrcb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2YCrCb
            )

            ycrcb[:, :, 0] = cv2.equalizeHist(
                ycrcb[:, :, 0]
            )

            result = cv2.cvtColor(
                ycrcb,
                cv2.COLOR_YCrCb2BGR
            )

        else:

            result = cv2.equalizeHist(image)

        return result, "Histogram equalization completed."

    # --------------------------------------------------------
    # THRESHOLDING
    # --------------------------------------------------------

    threshold_operations = {
        "threshold_binary": cv2.THRESH_BINARY,
        "threshold_inverse": cv2.THRESH_BINARY_INV,
        "threshold_trunc": cv2.THRESH_TRUNC,
        "threshold_zero": cv2.THRESH_TOZERO,
        "threshold_zi": cv2.THRESH_TOZERO_INV
    }

    if operation in threshold_operations:

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        threshold = int(
            form.get("threshold", 127)
        )

        threshold = max(
            0,
            min(255, threshold)
        )

        _, result = cv2.threshold(
            gray,
            threshold,
            255,
            threshold_operations[operation]
        )

        return result, f"Threshold value used: {threshold}."

    # --------------------------------------------------------
    # AVERAGING
    # --------------------------------------------------------

    if operation == "average":

        result = cv2.blur(
            image,
            (5, 5)
        )

        return result, "5x5 averaging filter applied."

    # --------------------------------------------------------
    # GAUSSIAN FILTER
    # --------------------------------------------------------

    if operation == "gaussian":

        result = cv2.GaussianBlur(
            image,
            (5, 5),
            0
        )

        return result, "5x5 Gaussian filter applied."

    # --------------------------------------------------------
    # MEDIAN FILTER
    # --------------------------------------------------------

    if operation == "median":

        result = cv2.medianBlur(
            image,
            5
        )

        return result, "5x5 median filter applied."

    # --------------------------------------------------------
    # BILATERAL FILTER
    # --------------------------------------------------------

    if operation == "bilateral":

        result = cv2.bilateralFilter(
            image,
            9,
            75,
            75
        )

        return result, "Bilateral filtering completed."

    # --------------------------------------------------------
    # GAUSSIAN NOISE REMOVAL
    # --------------------------------------------------------

    if operation == "gaussian_noise":

        result = cv2.GaussianBlur(
            image,
            (5, 5),
            0
        )

        return result, "Gaussian noise reduced using Gaussian filtering."

    # --------------------------------------------------------
    # SALT & PEPPER NOISE
    # --------------------------------------------------------

    if operation == "sp_noise":

        result = cv2.medianBlur(
            image,
            5
        )

        return result, "Salt-and-pepper noise reduced using median filtering."

    # --------------------------------------------------------
    # NON LOCAL MEANS
    # --------------------------------------------------------

    if operation == "nlm":

        result = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            10,
            10,
            7,
            21
        )

        return result, "Non-Local Means denoising completed."

    # --------------------------------------------------------
    # TELEA INPAINTING
    # --------------------------------------------------------

    if operation == "telea":

        mask = create_mask(image)

        result = cv2.inpaint(
            image,
            mask,
            3,
            cv2.INPAINT_TELEA
        )

        return result, "Telea inpainting applied using an automatic central mask."

    # --------------------------------------------------------
    # NAVIER-STOKES INPAINTING
    # --------------------------------------------------------

    if operation == "ns":

        mask = create_mask(image)

        result = cv2.inpaint(
            image,
            mask,
            3,
            cv2.INPAINT_NS
        )

        return result, "Navier-Stokes inpainting applied using an automatic central mask."

    # --------------------------------------------------------
    # JPEG COMPRESSION
    # --------------------------------------------------------

    if operation == "jpeg":

        quality = int(
            form.get("jpeg_quality", 30)
        )

        quality = max(
            1,
            min(100, quality)
        )

        success, encoded = cv2.imencode(
            ".jpg",
            image,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                quality
            ]
        )

        if not success:
            raise ValueError("JPEG compression failed.")

        result = cv2.imdecode(
            encoded,
            cv2.IMREAD_COLOR
        )

        return result, f"JPEG compression applied with quality {quality}."

    # --------------------------------------------------------
    # PNG COMPRESSION
    # --------------------------------------------------------

    if operation == "png":

        compression = int(
            form.get("png_compression", 9)
        )

        compression = max(
            0,
            min(9, compression)
        )

        success, encoded = cv2.imencode(
            ".png",
            image,
            [
                cv2.IMWRITE_PNG_COMPRESSION,
                compression
            ]
        )

        if not success:
            raise ValueError("PNG compression failed.")

        result = cv2.imdecode(
            encoded,
            cv2.IMREAD_COLOR
        )

        return result, f"PNG compression level {compression} applied."

    # --------------------------------------------------------
    # RLE
    # --------------------------------------------------------

    if operation == "rle":

        original, estimated = rle_estimate(image)

        ratio = (
            original / estimated
            if estimated > 0
            else 0
        )

        return image, (
            f"Educational RLE estimate completed. "
            f"Original units={original}, "
            f"estimated encoded units={estimated}, "
            f"ratio={ratio:.2f}."
        )

    # --------------------------------------------------------
    # LZW
    # --------------------------------------------------------

    if operation == "lzw":

        original, codes = lzw_estimate(image)

        ratio = (
            original / codes
            if codes > 0
            else 0
        )

        return image, (
            f"Educational LZW estimate completed. "
            f"Sample symbols={original}, "
            f"LZW codes={codes}, "
            f"ratio={ratio:.2f}."
        )

    # --------------------------------------------------------
    # MORPHOLOGY
    # --------------------------------------------------------

    if operation in [
        "erosion",
        "dilation",
        "opening",
        "closing"
    ]:

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, binary = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

        kernel = np.ones(
            (5, 5),
            np.uint8
        )

        if operation == "erosion":

            result = cv2.erode(
                binary,
                kernel,
                iterations=1
            )

            return result, "5x5 erosion applied."

        if operation == "dilation":

            result = cv2.dilate(
                binary,
                kernel,
                iterations=1
            )

            return result, "5x5 dilation applied."

        if operation == "opening":

            result = cv2.morphologyEx(
                binary,
                cv2.MORPH_OPEN,
                kernel
            )

            return result, "Morphological opening applied."

        if operation == "closing":

            result = cv2.morphologyEx(
                binary,
                cv2.MORPH_CLOSE,
                kernel
            )

            return result, "Morphological closing applied."

    # --------------------------------------------------------
    # CORRELATION / TEMPLATE MATCHING
    # --------------------------------------------------------

    if operation == "correlation":

        if second_image is None:

            h, w = image.shape[:2]

            crop_w = max(
                20,
                int(w * 0.30)
            )

            crop_h = max(
                20,
                int(h * 0.30)
            )

            x1 = max(
                0,
                w // 2 - crop_w // 2
            )

            y1 = max(
                0,
                h // 2 - crop_h // 2
            )

            template = image[
                y1:y1 + crop_h,
                x1:x1 + crop_w
            ]

        else:

            template = second_image

        gray_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray_template = cv2.cvtColor(
            template,
            cv2.COLOR_BGR2GRAY
        )

        th, tw = gray_template.shape[:2]

        ih, iw = gray_image.shape[:2]

        if th >= ih or tw >= iw:

            scale = min(
                (iw - 2) / tw,
                (ih - 2) / th
            )

            scale = max(
                0.05,
                scale
            )

            gray_template = cv2.resize(
                gray_template,
                None,
                fx=scale,
                fy=scale
            )

            th, tw = gray_template.shape[:2]

        result_match = cv2.matchTemplate(
            gray_image,
            gray_template,
            cv2.TM_CCOEFF_NORMED
        )

        _, max_value, _, max_location = cv2.minMaxLoc(
            result_match
        )

        x, y = max_location

        output = image.copy()

        cv2.rectangle(
            output,
            (x, y),
            (x + tw, y + th),
            (255, 255, 255),
            3
        )

        cv2.putText(
            output,
            f"Match: {max_value:.2f}",
            (x, max(25, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return output, (
            f"Template matching completed. "
            f"Correlation score={max_value:.3f}."
        )

    # --------------------------------------------------------
    # POST LAB COLOR SPACES
    # --------------------------------------------------------

    if operation == "post_hsv":

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        result = cv2.cvtColor(
            hsv,
            cv2.COLOR_HSV2BGR
        )

        return result, "HSV color-space conversion completed."

    if operation == "post_ycrcb":

        ycrcb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2YCrCb
        )

        result = cv2.cvtColor(
            ycrcb,
            cv2.COLOR_YCrCb2BGR
        )

        return result, "YCrCb color-space conversion completed."

    if operation == "post_lab":

        lab = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2LAB
        )

        result = cv2.cvtColor(
            lab,
            cv2.COLOR_LAB2BGR
        )

        return result, "Lab color-space conversion completed."

    # --------------------------------------------------------
    # CANNY
    # --------------------------------------------------------

    if operation == "post_canny":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        result = cv2.Canny(
            gray,
            100,
            200
        )

        return result, "Canny edge detection completed."

    # --------------------------------------------------------
    # SOBEL
    # --------------------------------------------------------

    if operation == "post_sobel":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        sx = cv2.Sobel(
            gray,
            cv2.CV_64F,
            1,
            0,
            ksize=3
        )

        sy = cv2.Sobel(
            gray,
            cv2.CV_64F,
            0,
            1,
            ksize=3
        )

        magnitude = cv2.magnitude(
            sx.astype(np.float32),
            sy.astype(np.float32)
        )

        result = cv2.normalize(
            magnitude,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)

        return result, "Sobel edge detection completed."

    # --------------------------------------------------------
    # PREWITT
    # --------------------------------------------------------

    if operation == "post_prewitt":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        kernel_x = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ], dtype=np.float32)

        kernel_y = np.array([
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
        ], dtype=np.float32)

        px = cv2.filter2D(
            gray,
            cv2.CV_32F,
            kernel_x
        )

        py = cv2.filter2D(
            gray,
            cv2.CV_32F,
            kernel_y
        )

        magnitude = cv2.magnitude(
            px,
            py
        )

        result = cv2.normalize(
            magnitude,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)

        return result, "Prewitt edge detection completed."

    raise ValueError(
        "Selected operation is not available."
    )


# ============================================================
# HTML / CSS / JAVASCRIPT
# ============================================================
