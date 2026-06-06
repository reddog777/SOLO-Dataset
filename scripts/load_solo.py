from scripts.load_solo import load_solo_tracedata

# Load a sample of 1000 traces
traces, metadata = load_solo_tracedata("path_to_solo_dataset.h5", num_traces=1000)

print(f"Loaded traces shape: {traces.shape}")
print(f"Sample ciphertext: {metadata['c'][0]}")