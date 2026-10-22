from src.case2.collatz_sequence import CollatzSequence
from src.case2.collatz_analyzer import CollatzAnalyzer


analyzer = CollatzAnalyzer(1, 100)
best: CollatzSequence = analyzer.longest()
print(f"{best.start}: {best.steps} steps, peak: {best.peak}")
