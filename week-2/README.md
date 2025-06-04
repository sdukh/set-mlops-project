# Data Annotation and Versioning System

## Overview

This project implements a complete MLOps pipeline for data annotation and versioning using Label Studio, MinIO, and DVC. The system provides efficient data labeling capabilities with proper version control for machine learning datasets.

## Dataset

This project uses a subset of the [Caltech-101 dataset](https://www.kaggle.com/datasets/imbikramsaha/caltech-101/code) from Kaggle, which contains images of objects belonging to 101 categories. The dataset is particularly suitable for object detection tasks.

## Architecture

The system consists of three main components:

1. **Label Studio** - Web-based data annotation tool
2. **MinIO** - Object storage for data management
3. **DVC** - Data version control system

## Tools Used

### Data Annotation Tool: Label Studio
- **Purpose**: Object detection with bounding boxes
- **Features**: 
  - Web-based interface
  - Support for multiple annotation types
  - Integration with cloud storage
  - Export capabilities in various formats (YOLO, COCO, etc.)

### Storage Solution: MinIO
- **Purpose**: S3-compatible object storage
- **Configuration**: Three buckets for different data stages
- **Features**: Local deployment, S3 API compatibility

### Version Control: DVC (Data Version Control)
- **Purpose**: Track and version large datasets
- **Features**: 
  - Git-like experience for data
  - Remote storage integration
  - Reproducible data pipelines

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Git

### Local Deployment

1. **Start the infrastructure:**
   ```bash
   docker compose up -d
   ```

2. **Access MinIO (http://localhost:9009/)**
   - Login: `minioadmin`
   - Password: `minioadmin`
   
   Create three buckets:
   - `cars-dataset` - for raw images
   - `cars-labeled-dataset` - for annotated data from Label Studio
   - `cars-dvc-storage` - for DVC versioned data

3. **Access Label Studio (http://localhost:8080/)**
   - Register an account
   - Create a new project
   - Select "Object Detection with Bounding Boxes"

### Label Studio Configuration

1. **Setup Cloud Storage Integration:**
   - Configure Source Cloud Storage:
     - URL: `http://minio:9000`
     - Bucket: `cars-dataset`
     - Enable "Treat every bucket object as a source file"
     - Disable pre-signed URLs
   
   - Configure Target Cloud Storage:
     - URL: `http://minio:9000`
     - Bucket: `cars-labeled-dataset`

2. **Upload and Annotate Data:**
   - Upload sample images to the `cars-dataset` bucket
   - Perform annotation using bounding boxes
   - Export annotated data

### DVC Setup

1. **Install DVC:**
   ```bash
   pip install 'dvc[all]'
   ```

2. **Initialize DVC:**
   ```bash
   dvc init
   mkdir -p dataset
   ```

3. **Configure Remote Storage:**
   ```bash
   dvc remote add -d storage s3://cars-dvc-storage
   dvc remote modify storage endpointurl http://localhost:9000
   
   # Set credentials
   export MINIO_ACCESS_KEY="minioadmin"
   export MINIO_SECRET_KEY="minioadmin"
   dvc remote modify storage --local access_key_id ${MINIO_ACCESS_KEY}
   dvc remote modify storage --local secret_access_key ${MINIO_SECRET_KEY}
   ```

4. **Commit initial configuration:**
   ```bash
   git add .dvc .gitignore
   git commit -m "Initialize DVC and storage setup"
   ```

## How to Run/Open Annotation

### Starting Annotation Process

1. **Launch the system:**
   ```bash
   docker compose up -d
   ```

2. **Open Label Studio:**
   - Navigate to http://localhost:8080/
   - Login to your account
   - Open your annotation project

3. **Begin annotation:**
   - Select images from the task list
   - Draw bounding boxes around objects of interest
   - Add appropriate labels
   - Submit annotations

### Exporting Annotations

1. **Manual export:**
   - In Label Studio, go to Export section
   - Choose desired format (YOLO, COCO, etc.)
   - Download the export

2. **Automated export using script:**
   ```bash
   export REFRESH_TOKEN=your_label_studio_token
   ./export_yolo.sh 1
   ```

## Dataset Versioning

### How Versioning Works

This project uses DVC for dataset versioning, which provides:

1. **Git-like workflow** for data
2. **Efficient storage** - only changes are stored
3. **Remote storage** integration with MinIO
4. **Reproducibility** - exact dataset versions can be restored

### Version Management Commands

1. **Add data to version control:**
   ```bash
   dvc add dataset
   git add dataset.dvc .gitignore
   git commit -m "v1 - initial dataset"
   dvc push
   ```

2. **Check status and differences:**
   ```bash
   dvc status
   dvc diff
   ```

3. **Create new version after updates:**
   ```bash
   # After adding more annotated data
   dvc add dataset
   git add dataset.dvc
   git commit -m "v2 - updated annotations"
   dvc push
   ```

4. **Restore previous version:**
   ```bash
   git log --oneline
   git checkout <commit-hash>
   dvc checkout
   ```

5. **Clone and restore data:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   
   # Setup credentials
   export MINIO_ACCESS_KEY="minioadmin"
   export MINIO_SECRET_KEY="minioadmin"
   dvc remote modify storage --local access_key_id ${MINIO_ACCESS_KEY}
   dvc remote modify storage --local secret_access_key ${MINIO_SECRET_KEY}
   
   # Download data
   dvc pull
   ```

## Planned Use Cases

This annotated dataset will be used for:

1. **Object Detection Model Training**
   - Training YOLO/other detection models
   - Transfer learning experiments
   - Model performance comparison

2. **Computer Vision Research**
   - Evaluation of different architectures
   - Augmentation technique testing
   - Few-shot learning experiments

3. **MLOps Pipeline Development**
   - Automated training pipelines
   - Model deployment strategies
   - Continuous integration for ML

## Project Structure

```
├── .dvc/                 # DVC configuration
├── dataset/              # Versioned dataset (not in git)
├── dataset.dvc           # DVC file tracking dataset
├── docker-compose.yml    # Infrastructure setup
├── export_yolo.sh        # Automated export script
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Future Improvements

- [ ] Automated annotation pipeline
- [ ] Integration with ML training workflows
- [ ] Advanced data validation
- [ ] Annotation quality metrics
- [ ] Multi-user annotation workflows

## Troubleshooting

### Common Issues

1. **MinIO connection issues**: Ensure Docker containers are running and ports are accessible
2. **DVC push/pull failures**: Check credentials and network connectivity to MinIO
3. **Label Studio storage errors**: Verify bucket permissions and URLs

### Support

For issues related to this project setup, please check the infrastructure logs:
```bash
docker compose logs
```

## License

This project is for educational purposes as part of the MLOps course assignment.