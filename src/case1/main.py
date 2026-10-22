from src.case1.collatz_sequence import CollatzSequence
from src.case1.collatz_analyzer import CollatzAnalyzer


analyzer = CollatzAnalyzer(1, 100)
best: CollatzSequence = analyzer.longest()
print(f"{best.start}: {best.steps} steps, peak: {best.peak}")

best_list = CollatzSequence(97)
print("The values: ", best_list.values)