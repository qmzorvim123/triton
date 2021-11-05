import numpy as np
import tritonclient.http as httpclient
import torch
from PIL import Image


if __name__ == '__main__':
    triton_client = httpclient.InferenceServerClient(url='172.17.0.2:8000')

    image = Image.open('cat.jpg')
    
    # replace with DALI Backend just for learning pipeline
    # the resized images maybe smaller, thus reduce network transimssion
    # the preprocess will do in the server side using DALI
    image = image.resize((224, 224), Image.ANTIALIAS)
    image = np.asarray(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    image = np.transpose(image, axes=[0, 3, 1, 2])
    image = image.astype(np.float32)

    inputs = []
    inputs.append(httpclient.InferInput('INPUT__0', image.shape, "FP32"))
    inputs[0].set_data_from_numpy(image, binary_data=False)
    outputs = []
    outputs.append(httpclient.InferRequestedOutput('OUTPUT__0', binary_data=False, class_count=1))

    results = triton_client.infer('resnet50_pytorch', inputs=inputs, outputs=outputs)
    output_data0 = results.as_numpy('OUTPUT__0')
    print(output_data0.shape)
    print(output_data0)
