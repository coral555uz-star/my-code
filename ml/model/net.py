import torch
import torch.nn.functional as F
import torch.nn as nn

class Net(torch.nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1=nn.Conv2d(1,64,3)
        self.conv2=nn.Conv2d(64,64,3)
        self.conv3=nn.Conv2d(64,128,3)
        self.conv4=nn.Conv2d(128,128,3)
        self.conv5=nn.Conv2d(128,256,3)
        self.conv6=nn.Conv2d(256,256,3)
        self.conv7=nn.Conv2d(256,512,3)
        self.conv8=nn.Conv2d(512,512,3)
        self.conv9=nn.Conv2d(512,1024,3)

        self.unconv1=nn.ConvTranspose2d(1024,512,2)
        self.unconv2=nn.ConvTranspose2d(512,256,2)
        self.unconv3=nn.ConvTranspose2d(256,128,2)
        self.unconv4=nn.ConvTranspose2d(128,64,2)
        self.final_conv=nn.ConvTranspose2d(64,2,1)


        self.maxpool=nn.MaxPool2d(2,2)
        self.relu=nn.ReLU(inplace=True)

    def forward(self,x):
        x=self.conv1(x)
        x=self.relu(x)
        x=self.maxpool(x)

        x=self.conv2(x)
        x=self.relu(x)
        x1=x
        x=self.maxpool(x)

        x=self.conv3(x)
        x=self.relu(x)
        x=self.maxpool(x)

        x=self.conv4(x)
        x=self.relu(x)
        x2=x
        x=self.maxpool(x)

        x=self.conv5(x)
        x=self.relu(x)
        x=self.maxpool(x)

        x=self.conv6(x)
        x=self.relu(x)
        x3=x
        x=self.maxpool(x)

        x=self.conv7(x)
        x=self.relu(x)
        x=self.maxpool(x)

        x=self.conv8(x)
        x=self.relu(x)
        x4=x
        x=self.maxpool(x)

        x=self.conv9(x)
        x=self.relu(x)
        x=self.maxpool(x)

        x=self.copyAndCrop(x4,x)
        x=self.unconv1(x)
        x=self.relu(x)

        x=self.copyAndCrop(x3,x)
        x=self.unconv2(x)
        x=self.relu(x)

        x=self.copyAndCrop(x2,x)
        x=self.unconv3(x)
        x=self.relu(x)

        x=self.copyAndCrop(x1,x)
        x=self.unconv4(x)
        x=self.relu(x)

        x=self.final_conv(x)
        return x
    
    def copyAndCrop(self,source,target):
        weight,height=target.size()[2],target.size()[3]
        source=source[:,:,:weight,:height]
        concat=torch.cat([source,target],dim=1)
        return concat





net=Net()
print(net)