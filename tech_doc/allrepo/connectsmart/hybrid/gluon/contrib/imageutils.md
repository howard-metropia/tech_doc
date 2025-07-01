# Gluon Contrib Image Utils Module

## Overview
Image processing utilities for web2py applications. Provides image resizing, thumbnail generation, and validation for upload fields using the Python PIL (Pillow) library.

## Module Information
- **Module**: `gluon.contrib.imageutils`
- **Dependencies**: PIL/Pillow, `gluon.current`
- **Purpose**: Image processing and thumbnail generation
- **Use Case**: Image upload validation and automatic resizing

## Key Features
- **Image Resizing**: Automatic resizing with aspect ratio preservation
- **Thumbnail Generation**: Create thumbnails from uploaded images
- **Quality Control**: Configurable JPEG quality settings
- **Padding Support**: Optional padding to maintain exact dimensions
- **GAE Compatible**: Google App Engine compatibility mode
- **Validation Integration**: Works as web2py field validator

## Classes and Functions

### RESIZE Class
Image resizing validator that can be used as a field requirement.

**Constructor:**
```python
def __init__(self, nx=160, ny=80, quality=100, padding=False, error_message=' image resize')
```

**Parameters:**
- `nx`: Maximum width in pixels (default: 160)
- `ny`: Maximum height in pixels (default: 80)
- `quality`: JPEG quality 1-100 (default: 100)
- `padding`: Add padding to maintain exact dimensions (default: False)
- `error_message`: Error message for validation failures

**Usage as Validator:**
```python
db.define_table('photos',
    Field('image', 'upload')
)

# Resize images to max 200x200
db.photos.image.requires = RESIZE(200, 200)

# With custom quality and padding
db.photos.image.requires = RESIZE(300, 200, quality=85, padding=True)
```

### RESIZE.__call__()
Main processing method called during validation.

**Signature:**
```python
def __call__(self, value)
```

**Parameters:**
- `value`: Upload field value (file-like object)

**Returns:**
- Tuple: `(processed_value, error_message)`
- `error_message` is None if successful

**Processing Steps:**
1. Open image using PIL
2. Create thumbnail maintaining aspect ratio
3. Apply padding if requested
4. Save as JPEG with specified quality
5. Replace original file content

**Aspect Ratio Handling:**
- Uses `Image.thumbnail()` which preserves aspect ratio
- Image is scaled to fit within specified dimensions
- Smaller dimension may be less than specified

**Padding Mode:**
- Creates background canvas of exact dimensions
- Centers resized image on background
- Background color: white (255, 255, 255, 0)

### THUMB Function
Generate thumbnail files from existing uploads.

**Signature:**
```python
def THUMB(image, nx=120, ny=120, gae=False, name='thumb')
```

**Parameters:**
- `image`: Original image filename
- `nx`: Thumbnail width (default: 120)
- `ny`: Thumbnail height (default: 120)
- `gae`: Google App Engine mode (default: False)
- `name`: Thumbnail suffix (default: 'thumb')

**Returns:**
- Thumbnail filename (non-GAE mode)
- Original filename (GAE mode)

**Usage as Computed Field:**
```python
db.define_table('photos',
    Field('image', 'upload'),
    Field('thumbnail', 'upload')
)

# Auto-generate thumbnail
db.photos.thumbnail.compute = lambda row: THUMB(row.image, 150, 150)
```

## Usage Examples

### Basic Image Resizing
```python
from gluon.contrib.imageutils import RESIZE

# Define table with image upload
db.define_table('products',
    Field('name', 'string'),
    Field('photo', 'upload')
)

# Automatically resize uploaded images
db.products.photo.requires = RESIZE(400, 300, quality=90)

# Controller
def add_product():
    form = FORM(
        INPUT(_name='name', _placeholder='Product Name'),
        INPUT(_name='photo', _type='file'),
        INPUT(_type='submit', _value='Add Product')
    )
    
    if form.process().accepted:
        # Image is automatically resized during processing
        product_id = db.products.insert(
            name=request.vars.name,
            photo=request.vars.photo
        )
        redirect(URL('view_product', args=[product_id]))
    
    return dict(form=form)
```

### Thumbnail Generation
```python
from gluon.contrib.imageutils import THUMB

# Table with automatic thumbnail generation
db.define_table('gallery',
    Field('title', 'string'),
    Field('image', 'upload'),
    Field('thumbnail', 'upload')
)

# Computed field for thumbnail
db.gallery.thumbnail.compute = lambda row: THUMB(row.image, 200, 200)

# Manual thumbnail generation
def create_thumbnail():
    image_filename = 'uploaded_image.jpg'
    thumb_filename = THUMB(image_filename, 100, 100, name='small')
    
    # thumb_filename will be 'uploaded_image_small.jpg'
    return thumb_filename
```

### Advanced Configuration
```python
# High-quality product images with padding
db.products.main_image.requires = RESIZE(
    nx=800, 
    ny=600, 
    quality=95, 
    padding=True,
    error_message='Image must be a valid format'
)

# Multiple thumbnail sizes
db.define_table('photos',
    Field('original', 'upload'),
    Field('large_thumb', 'upload'),
    Field('medium_thumb', 'upload'),
    Field('small_thumb', 'upload')
)

db.photos.large_thumb.compute = lambda row: THUMB(row.original, 300, 300, name='large')
db.photos.medium_thumb.compute = lambda row: THUMB(row.original, 150, 150, name='medium')
db.photos.small_thumb.compute = lambda row: THUMB(row.original, 75, 75, name='small')
```

### Error Handling
```python
def upload_with_validation():
    # Custom resize validator with error handling
    class CustomResize(RESIZE):
        def __call__(self, value):
            try:
                return super(CustomResize, self).__call__(value)
            except ImportError:
                return (value, 'PIL/Pillow library not installed')
            except Exception as e:
                return (value, 'Image processing failed: %s' % str(e))
    
    db.photos.image.requires = [
        IS_NOT_EMPTY(error_message='Please select an image'),
        CustomResize(400, 300, error_message='Invalid image format')
    ]
```

## Image Processing Details

### Supported Formats
- **Input**: Most PIL-supported formats (JPEG, PNG, GIF, BMP, TIFF)
- **Output**: JPEG format (configurable quality)
- **Transparency**: Lost during JPEG conversion

### Quality Settings
- **100**: Maximum quality (largest file size)
- **85-95**: High quality (recommended for photos)
- **70-85**: Good quality (balanced size/quality)
- **50-70**: Acceptable quality (smaller files)

### Memory Considerations
```python
# For large images, consider streaming processing
def process_large_image():
    # PIL automatically handles memory efficiently
    # But very large images may still cause memory issues
    db.photos.image.requires = RESIZE(1920, 1080, quality=85)
```

## GAE Compatibility

### Google App Engine Mode
```python
# GAE mode - returns original filename
thumbnail = THUMB('image.jpg', gae=True)
# Returns: 'image.jpg' (unchanged)

# Standard mode - creates actual thumbnail
thumbnail = THUMB('image.jpg', gae=False)  
# Returns: 'image_thumb.jpg' (new file created)
```

### GAE Limitations
- File system access limitations
- PIL availability may vary
- Consider using GAE's Images API instead

## File Organization

### Upload Structure
```
uploads/
├── image.jpg              # Original image
├── image_thumb.jpg        # Thumbnail
├── image_large.jpg        # Large thumbnail
└── image_small.jpg        # Small thumbnail
```

### Filename Convention
- Original: `filename.ext`
- Thumbnail: `filename_suffix.ext`
- Customizable suffix via `name` parameter

## Integration with Web2py

### Form Processing
```python
def process_form():
    form = crud.create(db.photos)
    
    if form.process().accepted:
        # Image automatically resized if RESIZE validator used
        # Thumbnail automatically generated if compute field defined
        response.flash = 'Photo uploaded and processed'
    
    return dict(form=form)
```

### Display Thumbnails
```python
# In view template
{{if record.thumbnail:}}
    <img src="{{=URL('default', 'download', args=[record.thumbnail])}}" 
         alt="Thumbnail" />
{{pass}}

# Or using helper
{{=IMG(_src=URL('default', 'download', args=[record.thumbnail]),
       _alt='Thumbnail', _class='thumbnail')}}
```

## Performance Considerations

### Processing Time
- Image processing adds upload time
- Larger images take longer to process
- Consider async processing for large images

### Storage Space
- Thumbnails increase storage requirements
- Multiple sizes multiply storage needs
- Consider cleanup strategies for old images

### Memory Usage
- PIL loads entire image into memory
- Very large images may cause memory issues
- Monitor memory usage in production

This module provides essential image processing capabilities for web2py applications, handling the common requirements of image resizing and thumbnail generation with configurable quality and sizing options.