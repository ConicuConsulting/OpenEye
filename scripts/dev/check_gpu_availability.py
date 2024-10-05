
import torch

def check_cuda():
    print("PyTorch CUDA Available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("CUDA Device Name:", torch.cuda.get_device_name(0))

if __name__ == "__main__":
    check_cuda()
