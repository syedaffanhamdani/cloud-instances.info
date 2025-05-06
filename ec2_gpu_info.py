def add_gpu_info(instances):
    """
    Add info about GPUs from the manually-curated dictionaries below. They are
    manually curated because GPU models and their corresponding CUDA Compute
    Capability are not listed in a structured form anywhere in the AWS docs.

    This function will print a warning if it encounters an instance with
    .GPU > 0 for which GPU information is not included in the dictionaries
    below. This may indicate that AWS has added a new GPU instance type. If you
    see such a warning and want to fill in the missing information, check
    https://aws.amazon.com/ec2/instance-types/#Accelerated_Computing for
    descriptions of the instance types and https://en.wikipedia.org/wiki/CUDA
    for information on the CUDA compute capability of different Nvidia GPU
    models.

    For G5 instances, please reference the following:
      https://aws.amazon.com/ec2/instance-types/g5/
      https://github.com/vantage-sh/ec2instances.info/issues/593
    """
    gpu_data = {
        "g2.2xlarge": {
            # No longer listed in AWS docs linked above. Alternative source is
            # https://medium.com/@manku_timma1/part-1-g2-2xlarge-gpu-basics-805ad40a37a4
            # The model has 2 units, 4G of memory each, but AWS exposes only 1 unit per instance
            "gpu_model": "NVIDIA GRID K520",
            "compute_capability": 3.0,
            "gpu_count": 1,
            "cuda_cores": 3072,
            "gpu_memory": 4,
        },
        "g2.8xlarge": {
            # No longer listed in AWS docs linked above. Alternative source is
            # https://aws.amazon.com/blogs/aws/new-g2-instance-type-with-4x-more-gpu-power/
            "gpu_model": "NVIDIA GRID K520",
            "compute_capability": 3.0,
            "gpu_count": 4,
            "cuda_cores": 6144,
            "gpu_memory": 16,
        },
        "g3s.xlarge": {
            "gpu_model": "NVIDIA Tesla M60",
            "compute_capability": 5.2,
            "gpu_count": 1,
            "cuda_cores": 2048,
            "gpu_memory": 8,
        },
        "g3.4xlarge": {
            "gpu_model": "NVIDIA Tesla M60",
            "compute_capability": 5.2,
            "gpu_count": 1,
            "cuda_cores": 2048,
            "gpu_memory": 8,
        },
        "g3.8xlarge": {
            "gpu_model": "NVIDIA Tesla M60",
            "compute_capability": 5.2,
            "gpu_count": 2,
            "cuda_cores": 4096,
            "gpu_memory": 16,
        },
        "g3.16xlarge": {
            "gpu_model": "NVIDIA Tesla M60",
            "compute_capability": 5.2,
            "gpu_count": 4,
            "cuda_cores": 8192,
            "gpu_memory": 32,
        },
        "g4dn.xlarge": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g4dn.2xlarge": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g4dn.4xlarge": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g4dn.8xlarge": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g4dn.16xlarge": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g4dn.12xlarge": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 4,
            "cuda_cores": 10240,
            "gpu_memory": 64,
        },
        "g4dn.metal": {
            "gpu_model": "NVIDIA T4 Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 8,
            "cuda_cores": 20480,
            "gpu_memory": 128,
        },
        "p2.xlarge": {
            "gpu_model": "NVIDIA Tesla K80",
            "compute_capability": 3.7,
            "gpu_count": 1,
            "cuda_cores": 2496,
            "gpu_memory": 12,
        },
        "p2.8xlarge": {
            "gpu_model": "NVIDIA Tesla K80",
            "compute_capability": 3.7,
            "gpu_count": 4,
            "cuda_cores": 19968,
            "gpu_memory": 96,
        },
        "p2.16xlarge": {
            "gpu_model": "NVIDIA Tesla K80",
            "compute_capability": 3.7,
            "gpu_count": 8,
            "cuda_cores": 39936,
            "gpu_memory": 192,
        },
        "p3.2xlarge": {
            "gpu_model": "NVIDIA Tesla V100",
            "compute_capability": 7.0,
            "gpu_count": 1,
            "cuda_cores": 5120,
            "gpu_memory": 16,
        },
        "p3.8xlarge": {
            "gpu_model": "NVIDIA Tesla V100",
            "compute_capability": 7.0,
            "gpu_count": 4,
            "cuda_cores": 20480,
            "gpu_memory": 64,
        },
        "p3.16xlarge": {
            "gpu_model": "NVIDIA Tesla V100",
            "compute_capability": 7.0,
            "gpu_count": 8,
            "cuda_cores": 40960,
            "gpu_memory": 128,
        },
        "p3dn.24xlarge": {
            "gpu_model": "NVIDIA Tesla V100",
            "compute_capability": 7.0,
            "gpu_count": 8,
            "cuda_cores": 40960,
            "gpu_memory": 256,
        },
        "g5.xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 1,
            "cuda_cores": 9616,
            "gpu_memory": 24,
        },
        "g5.2xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 1,
            "cuda_cores": 9616,
            "gpu_memory": 24,
        },
        "g5.4xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 1,
            "cuda_cores": 9616,
            "gpu_memory": 24,
        },
        "g5.8xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 1,
            "cuda_cores": 9616,
            "gpu_memory": 24,
        },
        "g5.16xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 1,
            "cuda_cores": 9616,
            "gpu_memory": 24,
        },
        "g5.12xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 4,
            "cuda_cores": 38464,
            "gpu_memory": 96,
        },
        "g5.24xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 4,
            "cuda_cores": 38464,
            "gpu_memory": 96,
        },
        "g5.48xlarge": {
            "gpu_model": "NVIDIA A10G",
            "compute_capability": 8.6,
            "gpu_count": 8,
            "cuda_cores": 76928,
            "gpu_memory": 192,
        },
        "g6.xlarge": {
            # GPU core count found from the whitepaper
            # https://images.nvidia.com/aem-dam/Solutions/Data-Center/l4/nvidia-ada-gpu-architecture-whitepaper-v2.1.pdf
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "g6.2xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "g6.4xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "g6.8xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "gr6.4xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "gr6.8xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "g6.16xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 7424,
            "gpu_memory": 24,
        },
        "g6.12xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 4,
            "cuda_cores": 29696,
            "gpu_memory": 96,
        },
        "g6.24xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 4,
            "cuda_cores": 29696,
            "gpu_memory": 96,
        },
        "g6.48xlarge": {
            "gpu_model": "NVIDIA L4",
            "compute_capability": 8.9,
            "gpu_count": 8,
            "cuda_cores": 59392,
            "gpu_memory": 192,
        },
        "p4d.24xlarge": {
            "gpu_model": "NVIDIA A100",
            "compute_capability": 8.0,
            "gpu_count": 8,
            "cuda_cores": 55296,  # Source: Asked Matthew Wilson at AWS as this isn't public anywhere.
            "gpu_memory": 320,
        },
        "p4de.24xlarge": {
            "gpu_model": "NVIDIA A100",
            "compute_capability": 8.0,
            "gpu_count": 8,
            "cuda_cores": 55296,
            "gpu_memory": 640,
        },
        "g5g.xlarge": {
            "gpu_model": "NVIDIA T4G Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g5g.2xlarge": {
            "gpu_model": "NVIDIA T4G Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g5g.4xlarge": {
            "gpu_model": "NVIDIA T4G Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g5g.8xlarge": {
            "gpu_model": "NVIDIA T4G Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 1,
            "cuda_cores": 2560,
            "gpu_memory": 16,
        },
        "g5g.16xlarge": {
            "gpu_model": "NVIDIA T4G Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 2,
            "cuda_cores": 5120,
            "gpu_memory": 32,
        },
        "g5g.metal": {
            "gpu_model": "NVIDIA T4G Tensor Core",
            "compute_capability": 7.5,
            "gpu_count": 2,
            "cuda_cores": 5120,
            "gpu_memory": 32,
        },
        "g4ad.xlarge": {
            "gpu_model": "AMD Radeon Pro V520",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 8,
        },
        "g4ad.2xlarge": {
            "gpu_model": "AMD Radeon Pro V520",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 8,
        },
        "g4ad.4xlarge": {
            "gpu_model": "AMD Radeon Pro V520",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 8,
        },
        "g4ad.8xlarge": {
            "gpu_model": "AMD Radeon Pro V520",
            "compute_capability": 0,
            "gpu_count": 2,
            "gpu_memory": 16,
        },
        "g4ad.16xlarge": {
            "gpu_model": "AMD Radeon Pro V520",
            "compute_capability": 0,
            "gpu_count": 4,
            "gpu_memory": 32,
        },
        "trn1.2xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 32,
        },
        "trn1.32xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 16,
            "gpu_memory": 512,
        },
        "trn1n.32xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 16,
            "gpu_memory": 512,
        },
        "inf1.xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 0,
        },
        "inf1.2xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 0,
        },
        "inf1.6xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 4,
            "gpu_memory": 0,
        },
        "inf1.24xlarge": {
            "gpu_model": "AWS Inferentia",
            "compute_capability": 0,
            "gpu_count": 16,
            "gpu_memory": 0,
        },
        "inf2.xlarge": {
            "gpu_model": "AWS Inferentia2",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 32,
        },
        "inf2.8xlarge": {
            "gpu_model": "AWS Inferentia2",
            "compute_capability": 0,
            "gpu_count": 1,
            "gpu_memory": 32,
        },
        "inf2.24xlarge": {
            "gpu_model": "AWS Inferentia2",
            "compute_capability": 0,
            "gpu_count": 6,
            "gpu_memory": 192,
        },
        "inf2.48xlarge": {
            "gpu_model": "AWS Inferentia2",
            "compute_capability": 0,
            "gpu_count": 12,
            "gpu_memory": 384,
        },
        "p5.48xlarge": {
            "gpu_model": "NVIDIA H100",
            "compute_capability": 9.0,
            "gpu_count": 8,
            "cuda_cores": 18432,
            "gpu_memory": 640,
        },
        # New entries for the missing instance types
        "g6e.xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 18176,  # Based on L40S specs
            "gpu_memory": 48,
        },
        "g6e.2xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 18176,
            "gpu_memory": 48,
        },
        "g6e.4xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 18176,
            "gpu_memory": 48,
        },
        "g6e.8xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 18176,
            "gpu_memory": 48,
        },
        "g6e.12xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 4,
            "cuda_cores": 72704,
            "gpu_memory": 192,
        },
        "g6e.16xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 1,
            "cuda_cores": 18176,
            "gpu_memory": 48,
        },
        "g6e.24xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 4,
            "cuda_cores": 72704,
            "gpu_memory": 192,
        },
        "g6e.48xlarge": {
            "gpu_model": "NVIDIA L40S Tensor Core",
            "compute_capability": 8.9,
            "gpu_count": 8,
            "cuda_cores": 145408,
            "gpu_memory": 384,
        },
        "p5e.48xlarge": {
            "gpu_model": "NVIDIA H200 Tensor Core",
            "compute_capability": 9.0,
            "gpu_count": 8,
            "cuda_cores": 18432,  # Same core count as H100
            "gpu_memory": 1128,  # Total memory across 8 GPUs (141GB per GPU)
        },
        "p5en.48xlarge": {
            "gpu_model": "NVIDIA H200 Tensor Core",
            "compute_capability": 9.0,
            "gpu_count": 8,
            "cuda_cores": 18432,
            "gpu_memory": 1128,
        },
        "trn2.48xlarge": {
            "gpu_model": "AWS Trainium2",
            "compute_capability": 0,  # Not NVIDIA CUDA
            "gpu_count": 16,  # 16 Trainium2 chips
            "cuda_cores": 0,  # Not applicable for AWS custom chips
            "gpu_memory": 1536,  # 1.5TB high bandwidth memory
        },
    }
    for inst in instances:
        if inst.GPU == 0:
            continue
        if inst.instance_type not in gpu_data:
            print(
                f"WARNING: instance {inst.instance_type} has GPUs but is missing from gpu_data "
                "dict in scrape.add_gpu_info. The dict needs to be updated manually."
            )
            continue
        inst_gpu_data = gpu_data[inst.instance_type]
        inst.GPU = inst_gpu_data["gpu_count"]
        inst.GPU_model = inst_gpu_data["gpu_model"]
        inst.compute_capability = inst_gpu_data["compute_capability"]
        inst.GPU_memory = inst_gpu_data["gpu_memory"]
