# Upload Tools Module Documentation

## Overview
The Upload Tools Module provides comprehensive file upload functionality for the ConnectSmart Hybrid Portal application. It supports both AWS S3 cloud storage and local file system storage, with specialized handling for image uploads and base64 encoding support.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/upload_tools.py`

## Dependencies
- `os`: File system operations
- `io`: In-memory file operations
- `base64`: Base64 encoding/decoding
- `logging`: Error and debug logging
- `boto3`: AWS S3 client (imported when needed)
- `botocore.exceptions.ClientError`: AWS error handling
- `PIL.Image`: Image processing (imported when needed)
- `gluon.current`: Web2py current context

## Module Exports
```python
__all__ = ['UploadTool']
```

## Global Configuration
```python
logger = logging.getLogger(__name__)
```

## Classes

### UploadTool

#### Purpose
Main class for handling file uploads to both AWS S3 and local file system with automatic storage selection and image processing capabilities.

#### Constructor
```python
def __init__(self, aws_s3_bucket=None)
```

**Parameters**:
- `aws_s3_bucket` (str, optional): AWS S3 bucket name for cloud storage

**Storage Selection**:
- **AWS S3**: When `aws_s3_bucket` is provided
- **Local Storage**: When `aws_s3_bucket` is None or empty

#### Methods

##### `_upload_to_s3(self, target_path, streams)`
**Purpose**: Private method for uploading files to AWS S3
**Parameters**:
- `target_path` (str): Target file path within S3 bucket
- `streams` (io.BytesIO): File content stream

**Returns**: S3 URL string or empty string on error

**Process**:
1. Create S3 client using boto3
2. Upload file content to specified bucket and path
3. Determine bucket location for URL generation
4. Return full S3 URL or empty string on error

**URL Format**:
```python
'https://s3-{region}.amazonaws.com/{bucket}/{key}'
```

**Error Handling**:
- Catches `ClientError` exceptions
- Logs errors with S3 prefix
- Returns empty string on failure

##### `upload_image(self, target_path, image)`
**Purpose**: Upload PIL Image object to configured storage
**Parameters**:
- `target_path` (str): Target file path
- `image` (PIL.Image): Image object to upload

**Returns**: URL string pointing to uploaded image

**Process**:
1. Convert image to JPEG format
2. Save to in-memory BytesIO stream
3. Choose storage method based on S3 configuration
4. Handle directory creation for local storage
5. Return access URL for uploaded image

**Storage Paths**:
- **S3**: Direct path within bucket
- **Local**: `static/images/{target_path}` within Web2py application

##### `upload_base64_image(self, target_path, str_base64)`
**Purpose**: Upload base64-encoded image string
**Parameters**:
- `target_path` (str): Target file path
- `str_base64` (str): Base64-encoded image data

**Returns**: URL string pointing to uploaded image

**Process**:
1. Decode base64 string to binary data
2. Create PIL Image from binary data
3. Convert to RGB format
4. Log image metadata (format, size, mode)
5. Call `upload_image()` with processed image

**Error Handling**:
- Catches `TypeError` for invalid base64 data
- Logs decoding errors
- Re-raises exceptions for caller handling

## Storage Implementations

### AWS S3 Storage

#### Configuration
```python
# Requires AWS credentials configured via:
# - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# - IAM roles
# - AWS credentials file
```

#### S3 Operations
```python
import boto3
from botocore.exceptions import ClientError

client = boto3.client('s3')
client.put_object(Bucket=bucket, Key=key, Body=streams.getvalue())
```

#### URL Generation
```python
bucket_location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']
url = f'https://s3-{bucket_location}.amazonaws.com/{bucket}/{key}'
```

### Local File System Storage

#### Directory Structure
```
application_root/
├── static/
│   └── images/
│       └── {target_path}/
│           └── uploaded_files
```

#### File Operations
```python
# Create directory structure
folder_path = os.path.join(current.request.folder, folder)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Save image file
image.save(file_path, 'JPEG')
```

#### URL Generation
```python
url = os.path.join(
    current.request.env.http_host,
    current.request.application,
    folder,
    filename
)
```

## Usage Examples

### Basic S3 Upload
```python
# Initialize with S3 bucket
upload_tool = UploadTool(aws_s3_bucket='my-app-uploads')

# Upload PIL Image
from PIL import Image
image = Image.open('local_image.jpg')
url = upload_tool.upload_image('user_avatars/user_123.jpg', image)
print(f"Image uploaded to: {url}")
```

### Local Storage Upload
```python
# Initialize without S3 bucket (local storage)
upload_tool = UploadTool()

# Upload image to local storage
image = Image.open('profile_pic.png')
url = upload_tool.upload_image('profiles/user_456.jpg', image)
print(f"Image saved locally: {url}")
```

### Base64 Image Upload
```python
# Upload base64-encoded image
base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M+AAQACAAHVrZoM"

try:
    url = upload_tool.upload_base64_image('uploads/decoded_image.jpg', base64_data)
    print(f"Base64 image uploaded: {url}")
except TypeError as e:
    print(f"Invalid base64 data: {e}")
```

### Profile Picture Upload
```python
def upload_user_avatar(user_id, image_data):
    upload_tool = UploadTool(aws_s3_bucket='user-content')
    
    # Generate unique filename
    target_path = f'avatars/{user_id}/profile_{int(time.time())}.jpg'
    
    try:
        if image_data.startswith('data:image'):
            # Extract base64 part from data URL
            base64_data = image_data.split(',')[1]
            url = upload_tool.upload_base64_image(target_path, base64_data)
        else:
            # Handle PIL Image object
            url = upload_tool.upload_image(target_path, image_data)
            
        return {'success': True, 'url': url}
        
    except Exception as e:
        logger.error(f"Avatar upload failed for user {user_id}: {e}")
        return {'success': False, 'error': str(e)}
```

### Vehicle Photo Upload
```python
def upload_vehicle_photos(user_id, front_image, side_image):
    upload_tool = UploadTool(aws_s3_bucket='vehicle-photos')
    
    results = {}
    
    try:
        # Upload front photo
        front_path = f'vehicles/{user_id}/front.jpg'
        results['front_url'] = upload_tool.upload_image(front_path, front_image)
        
        # Upload side photo
        side_path = f'vehicles/{user_id}/side.jpg'
        results['side_url'] = upload_tool.upload_image(side_path, side_image)
        
        return results
        
    except Exception as e:
        logger.error(f"Vehicle photo upload failed: {e}")
        raise
```

## Image Processing Features

### Format Conversion
- **Output Format**: JPEG (standardized)
- **Quality**: Default PIL JPEG quality
- **Compression**: Automatic compression applied

### Color Space Conversion
```python
# Base64 images converted to RGB
im = im.convert('RGB')
```

### Metadata Logging
```python
logger.debug('Image format={}, size={}, mode={}'.format(
    im.format, im.size, im.mode))
```

## Error Handling Patterns

### S3 Upload Errors
```python
try:
    client.put_object(Bucket=bucket, Key=key, Body=streams.getvalue())
    return url
except ClientError as e:
    logger.error('[S3] {}'.format(e.message))
    return ''
```

### Base64 Decoding Errors
```python
try:
    decoded_str = base64.b64decode(str_base64)
except TypeError as e:
    logger.error('Image base64 decode error: {}'.format(e.message))
    raise e
```

### File System Errors
```python
# Directory creation
if not os.path.exists(folder_path):
    os.makedirs(folder_path)  # May raise OSError

# File writing
image.save(file_path, 'JPEG')  # May raise IOError
```

## Configuration Examples

### AWS S3 Configuration
```python
# Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2

# Bucket configuration
upload_tool = UploadTool(aws_s3_bucket='my-app-uploads-prod')
```

### Local Storage Configuration
```python
# Web2py application structure
application/
├── static/
│   └── images/        # Upload directory
├── controllers/
├── models/
└── views/

# No additional configuration needed
upload_tool = UploadTool()  # Defaults to local storage
```

## Security Considerations

### S3 Security
- **IAM Permissions**: Minimum required permissions for S3 operations
- **Bucket Policies**: Restrict access to authorized users
- **Encryption**: Consider S3 server-side encryption
- **Access Logging**: Enable S3 access logging for auditing

### File System Security
- **Directory Permissions**: Restrict write access to upload directories
- **File Validation**: Validate file types and sizes
- **Path Traversal**: Prevent directory traversal attacks
- **Disk Space**: Monitor disk usage for upload directory

### Image Processing Security
- **File Type Validation**: Ensure uploaded files are valid images
- **Size Limits**: Implement maximum file size restrictions
- **Content Scanning**: Consider malware scanning for uploads
- **Metadata Stripping**: Remove potentially sensitive EXIF data

## Performance Considerations

### Memory Usage
- **Stream Processing**: Uses BytesIO for efficient memory usage
- **Image Conversion**: PIL processing in memory
- **Large Files**: Consider streaming for large image uploads

### Network Performance
- **S3 Transfer**: Direct upload to S3 without local caching
- **Parallel Uploads**: Consider async uploads for multiple files
- **CDN Integration**: Use CloudFront for S3-hosted images

## Integration Patterns

### Web2py Integration
```python
def upload_handler():
    if request.vars.image:
        upload_tool = UploadTool(aws_s3_bucket=settings.s3_bucket)
        
        # Handle file upload
        uploaded_file = request.vars.image
        image = Image.open(uploaded_file.file)
        
        # Generate target path
        target_path = f'uploads/{auth.user.id}/{uploaded_file.filename}'
        
        # Upload and get URL
        url = upload_tool.upload_image(target_path, image)
        
        # Save URL to database
        db.user_uploads.insert(
            user_id=auth.user.id,
            filename=uploaded_file.filename,
            url=url
        )
        
        return dict(success=True, url=url)
```

### API Integration
```python
@request.restful()
def upload_api():
    def POST():
        try:
            # Validate request
            if 'image' not in request.vars:
                raise HTTP(400, "No image provided")
                
            # Process upload
            upload_tool = UploadTool(aws_s3_bucket=myconf.get('s3.bucket'))
            
            # Handle base64 or file upload
            if request.vars.image.startswith('data:'):
                base64_data = request.vars.image.split(',')[1]
                url = upload_tool.upload_base64_image(
                    f'api_uploads/{uuid.uuid4()}.jpg',
                    base64_data
                )
            else:
                # Handle file object
                pass
                
            return dict(success=True, url=url)
            
        except Exception as e:
            logger.error(f"Upload API error: {e}")
            raise HTTP(500, "Upload failed")
    
    return locals()
```

## Related Components
- User profile management
- Vehicle registration system
- Content management system
- CDN integration
- Image optimization services