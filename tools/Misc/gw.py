import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Make sure char_to_idx and idx_to_char are defined

def generate_candidates(model, seed='', char_to_idx=char_to_idx, idx_to_char=idx_to_char,
                        max_len=11, num_candidates=5, temperature=1.0, log_file='log.txt'):
    """
    Generate multiple candidate IDs with progress printing and logging.
    """
    candidates = []

    with open(log_file, 'w') as log:
        log.write("Candidate Generation Log\n")
        log.write("=======================\n")

    for i in range(num_candidates):
        seq = seed
        for _ in range(max_len - len(seed)):
            # Encode current sequence
            x = [char_to_idx[c] for c in seq]
            x = pad_sequences([x], maxlen=max_len-1, padding='pre')

            # Predict next char probabilities
            preds = model.predict(x, verbose=0)[0]
            
            # Apply temperature
            preds = np.asarray(preds).astype('float64')
            preds = np.log(preds + 1e-8) / temperature
            exp_preds = np.exp(preds)
            preds = exp_preds / np.sum(exp_preds)

            # Sample next character
            next_idx = np.random.choice(len(preds), p=preds)
            seq += idx_to_char[next_idx]

        candidates.append(seq)
        
        # Print progress
        print(f"[INFO] Generated candidate {i+1}/{num_candidates}: {seq}")

        # Log candidate
        with open(log_file, 'a') as log:
            log.write(f"Candidate {i+1}: {seq}\n")
    
    return candidates

def rank_candidates(model, candidates, char_to_idx=char_to_idx, max_len=11, log_file='log.txt'):
    """
    Rank candidate IDs by model likelihood with logging.
    """
    scores = []
    with open(log_file, 'a') as log:
        log.write("\nCandidate Ranking Log\n")
        log.write("====================\n")

    for i, cand in enumerate(candidates):
        score = 0
        for j in range(1, len(cand)):
            seq = [char_to_idx[c] for c in cand[:j]]
            x = pad_sequences([seq], maxlen=max_len-1, padding='pre')
            pred = model.predict(x, verbose=0)[0]
            score += np.log(pred[char_to_idx[cand[j]]] + 1e-8)  # log-likelihood
        scores.append(score)

        # Print and log progress
        print(f"[INFO] Candidate {i+1}/{len(candidates)} log-likelihood: {score:.4f}")
        with open(log_file, 'a') as log:
            log.write(f"Candidate {i+1}: {cand} | Log-likelihood: {score:.4f}\n")

    # Sort descending
    ranked = [c for _, c in sorted(zip(scores, candidates), reverse=True)]
    with open(log_file, 'a') as log:
        log.write("\nRanked Candidates:\n")
        for i, c in enumerate(ranked):
            log.write(f"{i+1}: {c}\n")
    
    return ranked

# Example usage
seed = ''
candidates = generate_candidates(model, seed=seed, num_candidates=10, temperature=0.8)
ranked_candidates = rank_candidates(model, candidates)

print("\nTop candidates:")
for c in ranked_candidates[:5]:
    print(c)