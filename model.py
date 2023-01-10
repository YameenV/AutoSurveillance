import torch as th

def loadModel(path:str):
    model = th.hub.load("WongKinYiu/yolov7","custom",f"{path}",trust_repo=True)
    return model

if __name__ == "__main__":
    loadModel()