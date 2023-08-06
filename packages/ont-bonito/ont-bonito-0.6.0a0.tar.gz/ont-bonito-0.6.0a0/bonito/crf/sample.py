import torch


def update_state(state, base, n_base, n_state):
    return torch.where(base == 0, state, (state * n_base) % n_state + base - 1)


def sample(init_state, trans_probs, n_sample):
    T, N, n_state, C = trans_probs.shape
    n_base = C - 1

    bases = [] #should we add the bases from init_state?
    
    state = init_state    
    for t in range(T):
        p = torch.gather(trans_probs[t], 1, state[:,:,None].expand(-1,-1, n_base + 1))
        base = torch.multinomial(p.reshape(-1, n_base + 1), 1).reshape(-1, n_sample)
        state = update_state(state, base, n_base, n_state) 
        bases.append(base)   
    
    return torch.stack(bases, dim=1)


def get_samples(b, t, n_sample=16, beta=1.0):
    with torch.no_grad():
        init_state_probs = torch.tensor(b, device=device).unsqueeze(0)
        trans_probs = torch.tensor(t, device=device).unsqueeze(1)
        if beta != 1.0:
            trans_probs = torch.pow(trans_probs, beta)
            trans_probs /= trans_probs.sum(-1, keepdim=True)
        init_state = torch.multinomial(init_state_probs, n_sample)
        bases = sample(init_state, trans_probs, n_sample)
    
    bases = bases.cpu().numpy()[0]
    return [''.join(['_ACGT'[i] for i in bases[:, n] if i != 0]) for n in range(n_sample)]
