from flask import Flask, render_template, request, jsonify
import time
import random
from typing import List, Dict

app = Flask(__name__)

class SortingVisualizer:
    def __init__(self):
        self.steps = []
    
    def generate_random_array(self, size: int = 50) -> List[int]:
        return random.sample(range(1, size + 1), size)
    
    def bubble_sort(self, arr: List[int]) -> List[Dict]:
        """Bubble Sort with step-by-step visualization"""
        n = len(arr)
        steps = []
        arr_copy = arr.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight compared elements
                steps.append({
                    "array": arr_copy.copy(),
                    "compared": [j, j + 1],
                    "sorted": list(range(n - i, n))
                })
                
                if arr_copy[j] > arr_copy[j + 1]:
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    steps.append({
                        "array": arr_copy.copy(),
                        "swapped": [j, j + 1],
                        "sorted": list(range(n - i, n))
                    })
        
        steps.append({"array": arr_copy, "sorted": list(range(n))})
        return steps
    
    def selection_sort(self, arr: List[int]) -> List[Dict]:
        """Selection Sort with visualization"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        for i in range(n):
            min_idx = i
            steps.append({
                "array": arr_copy.copy(),
                "min_index": min_idx,
                "current": i,
                "sorted": list(range(i))
            })
            
            for j in range(i + 1, n):
                steps.append({
                    "array": arr_copy.copy(),
                    "compared": [min_idx, j],
                    "current": i,
                    "sorted": list(range(i))
                })
                
                if arr_copy[j] < arr_copy[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
                steps.append({
                    "array": arr_copy.copy(),
                    "swapped": [i, min_idx],
                    "sorted": list(range(i + 1))
                })
        
        steps.append({"array": arr_copy, "sorted": list(range(n))})
        return steps
    
    def insertion_sort(self, arr: List[int]) -> List[Dict]:
        """Insertion Sort with visualization"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        for i in range(1, n):
            key = arr_copy[i]
            j = i - 1
            
            steps.append({
                "array": arr_copy.copy(),
                "current": i,
                "key": key,
                "sorted": list(range(i))
            })
            
            while j >= 0 and arr_copy[j] > key:
                arr_copy[j + 1] = arr_copy[j]
                steps.append({
                    "array": arr_copy.copy(),
                    "shifting": j,
                    "key_position": j + 1,
                    "sorted": list(range(i))
                })
                j -= 1
            
            arr_copy[j + 1] = key
            steps.append({
                "array": arr_copy.copy(),
                "placed": j + 1,
                "sorted": list(range(i + 1))
            })
        
        steps.append({"array": arr_copy, "sorted": list(range(n))})
        return steps
    
    def merge_sort(self, arr: List[int]) -> List[Dict]:
        """Merge Sort with visualization"""
        steps = []
        arr_copy = arr.copy()
        
        def merge_sort_helper(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                
                # Show division
                steps.append({
                    "array": arr.copy(),
                    "dividing": list(range(left, right + 1)),
                    "mid": mid
                })
                
                merge_sort_helper(arr, left, mid)
                merge_sort_helper(arr, mid + 1, right)
                merge(arr, left, mid, right)
        
        def merge(arr, left, mid, right):
            # Show merging
            steps.append({
                "array": arr.copy(),
                "merging": list(range(left, right + 1)),
                "left_part": list(range(left, mid + 1)),
                "right_part": list(range(mid + 1, right + 1))
            })
            
            left_arr = arr[left:mid + 1]
            right_arr = arr[mid + 1:right + 1]
            
            i = j = 0
            k = left
            
            while i < len(left_arr) and j < len(right_arr):
                steps.append({
                    "array": arr.copy(),
                    "comparing": [left + i, mid + 1 + j],
                    "merging": list(range(left, right + 1))
                })
                
                if left_arr[i] <= right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                k += 1
            
            while i < len(left_arr):
                arr[k] = left_arr[i]
                i += 1
                k += 1
            
            while j < len(right_arr):
                arr[k] = right_arr[j]
                j += 1
                k += 1
            
            steps.append({
                "array": arr.copy(),
                "merged": list(range(left, right + 1))
            })
        
        merge_sort_helper(arr_copy, 0, len(arr_copy) - 1)
        steps.append({"array": arr_copy, "sorted": list(range(len(arr_copy)))})
        return steps
    
    def quick_sort(self, arr: List[int]) -> List[Dict]:
        """Quick Sort with visualization"""
        steps = []
        arr_copy = arr.copy()
        
        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)
        
        def partition(arr, low, high):
            pivot = arr[high]
            steps.append({
                "array": arr.copy(),
                "pivot": high,
                "current_partition": list(range(low, high + 1))
            })
            
            i = low - 1
            
            for j in range(low, high):
                steps.append({
                    "array": arr.copy(),
                    "comparing": [j, high],
                    "pivot": high,
                    "i_index": i,
                    "current_partition": list(range(low, high + 1))
                })
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if i != j:
                        steps.append({
                            "array": arr.copy(),
                            "swapped": [i, j],
                            "pivot": high,
                            "current_partition": list(range(low, high + 1))
                        })
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            steps.append({
                "array": arr.copy(),
                "pivot_placed": i + 1,
                "swapped": [i + 1, high],
                "current_partition": list(range(low, high + 1))
            })
            
            return i + 1
        
        quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
        steps.append({"array": arr_copy, "sorted": list(range(len(arr_copy)))})
        return steps

# Initialize sorter
sorter = SortingVisualizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_array', methods=['POST'])
def generate_array():
    size = request.json.get('size', 50)
    array = sorter.generate_random_array(size)
    return jsonify({'array': array})

@app.route('/sort', methods=['POST'])
def sort_array():
    print("✅ Sort endpoint called")
    data = request.json
    array = data['array']
    algorithm = data.get('algorithm', 'bubble')
    
    print(f"✅ Sorting array with {algorithm} sort")
    
    start_time = time.time()
    
    if algorithm == 'bubble':
        steps = sorter.bubble_sort(array)
    elif algorithm == 'selection':
        steps = sorter.selection_sort(array)
    elif algorithm == 'insertion':
        steps = sorter.insertion_sort(array)
    elif algorithm == 'merge':
        steps = sorter.merge_sort(array)
    elif algorithm == 'quick':
        steps = sorter.quick_sort(array)
    else:
        return jsonify({'error': 'Invalid algorithm'})
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"✅ Generated {len(steps)} steps in {execution_time:.2f} seconds")
    
    return jsonify({
        'steps': steps,
        'execution_time': execution_time 
    })

if __name__ == '__main__':
    print("🚀 Sorting Visualizer starting...")
    print("🌐 Open http://localhost:5000")
    app.run(debug=True)