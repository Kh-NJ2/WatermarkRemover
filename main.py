from pdf2image import convert_from_path
import cv2
import numpy as np
import os


def convert(path, dpi=68):
    """Convert PDF to PNG images"""
    try:
        # Remove hardcoded poppler path - let it use system PATH
        images = convert_from_path(path, dpi=dpi)
        
        for i, image in enumerate(images):
            filename = f"page_{i}.png"
            image.save(filename, "PNG")
            print(f"Saved: {filename}")
            
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return False
    return True


def show_img(path):
    """Display an image"""
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found")
        return
        
    image = cv2.imread(path, 0)
    if image is None:
        print(f"Error: Could not load image from '{path}'")
        return
        
    cv2.imshow("Original", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def remove_watermark(path_img, path_wm, threshold=0.8):
    """Remove watermark from image using template matching"""
    # Check if files exist
    if not os.path.exists(path_img):
        print(f"Error: Image file '{path_img}' not found")
        return
        
    if not os.path.exists(path_wm):
        print(f"Error: Watermark file '{path_wm}' not found")
        return
    
    # Load images
    image = cv2.imread(path_img)
    watermark = cv2.imread(path_wm, 0)
    
    if image is None:
        print(f"Error: Could not load image from '{path_img}'")
        return
        
    if watermark is None:
        print(f"Error: Could not load watermark from '{path_wm}'")
        return
    
    # Convert main image to grayscale for template matching
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Template matching
    result = cv2.matchTemplate(gray, watermark, cv2.TM_CCOEFF_NORMED)
    
    # Find all matches above threshold
    locations = np.where(result >= threshold)
    
    if len(locations[0]) == 0:
        print(f"No watermark found with threshold {threshold}")
        return
    
    h, w = watermark.shape
    
    # Create a copy for watermark removal
    cleaned_image = image.copy()
    
    # Remove watermarks by inpainting
    for pt in zip(*locations[::-1]):  # Switch x and y coordinates
        # Create mask for inpainting
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.rectangle(mask, pt, (pt[0] + w, pt[1] + h), 255, -1)
        
        # Inpaint the watermark area
        cleaned_image = cv2.inpaint(cleaned_image, mask, 3, cv2.INPAINT_TELEA)
        
        # Draw rectangle on original for visualization
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    
    # Display results
    cv2.imshow("Detected Watermarks", image)
    cv2.imshow("Cleaned Image", cleaned_image)
    
    # Save cleaned image
    output_path = "cleaned_" + os.path.basename(path_img)
    cv2.imwrite(output_path, cleaned_image)
    print(f"Cleaned image saved as: {output_path}")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """Main function with menu options"""
    print("PDF Watermark Removal Tool")
    print("1. Convert PDF to images")
    print("2. Show image")
    print("3. Remove watermark")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            path = input("Enter the path of the PDF: ").strip()
            dpi = int(input("Enter desrired dpi (default:68): "))
            if os.path.exists(path):
                if not dpi:  # If user just pressed Enter
                    dpi = 68
                else:
                    convert(path, dpi)
            else:
                print("PDF file not found!")
                
        elif choice == "2":
            path = input("Enter the path of the image: ").strip()
            show_img(path)
            
        elif choice == "3":
            img_path = input("Enter the path of the image: ").strip()
            wm_path = input("Enter the path of the watermark: ").strip()
            threshold = input("Enter threshold (0.0-1.0, default 0.8): ").strip()
            
            if threshold:
                try:
                    threshold = float(threshold)
                    if not 0.0 <= threshold <= 1.0:
                        print("Threshold must be between 0.0 and 1.0")
                        continue
                except ValueError:
                    print("Invalid threshold value")
                    continue
            else:
                threshold = 0.8
                
            remove_watermark(img_path, wm_path, threshold)
            
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()