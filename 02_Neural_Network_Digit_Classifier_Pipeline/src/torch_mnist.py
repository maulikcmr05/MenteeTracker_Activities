import torch
from torch import nn
from torch.utils.data import DataLoader,random_split
from torchvision import datasets,transforms
class Net(nn.Module):
    def __init__(self):
        super().__init__(); self.net=nn.Sequential(nn.Flatten(),nn.Linear(784,128),nn.Tanh(),nn.Linear(128,10))
    def forward(self,x): return self.net(x)
d=datasets.MNIST("data",train=True,download=True,transform=transforms.ToTensor())
tr,va=random_split(d,[54000,6000]); tl=DataLoader(tr,batch_size=128,shuffle=True); vl=DataLoader(va,batch_size=256)
m=Net(); opt=torch.optim.Adam(m.parameters()); loss=nn.CrossEntropyLoss()
for ep in range(3):
    m.train(); total=0
    for x,y in tl:
        opt.zero_grad(); z=loss(m(x),y); z.backward(); opt.step(); total+=z.item()
    m.eval(); good=n=0
    with torch.no_grad():
        for x,y in vl: good+=(m(x).argmax(1)==y).sum().item(); n+=len(y)
    print(ep+1,total/len(tl),good/n)
