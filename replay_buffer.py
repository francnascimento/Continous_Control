from collections import deque, namedtuple
import numpy as np

class ReplayBuffer():
    def __init__(self, buffer_size, batch_size):
        self.buffer_size=buffer_size
        self.batch_size = batch_size
        self.memory = deque(maxlen=self.buffer_size)
        self.experience= namedtuple('Experience', field_names=['state', 'action', 'reward', 'next_state', 'done' ])
        
    def add(self, state, action, reward, next_state, done):
        new_experience = self.experience(state, action, reward, next_state, done)
        self.memory.append(new_experience)
        
    def sample(self):
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(self.device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).float().to(self.device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(self.device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(self.device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(self.device)

        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)