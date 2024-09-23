import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

class PolicyGradientNN(nn.Module):
    def __init__(self, inputs: int, outputs: int):
        super(PolicyGradientNN, self).__init__()
        self.fc1 = nn.Linear(inputs, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, outputs)
        self.old = None

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x, dim=-1)
    def refit(self, reward: float, old_vector: list[float]):
        optimizer = optim.Adam(self.parameters(), lr=0.01)
        output_probs = self(old_vector)
        
        action = torch.multinomial(output_probs, num_samples=1)
        
        loss = -torch.log(output_probs.squeeze(0)[action]) * reward
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    def save(self):
        torch.save(self.state_dict(), "model_state.pth")

def init_model(observations: int, actions: int) -> PolicyGradientNN:
    model = PolicyGradientNN(observations, actions)
    

    return model

if __name__ == '__main__':
    model = init_model(1, 2)
    input = torch.randn(1, 1)
    out = model(input)
    
    print(out)