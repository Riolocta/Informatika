import heapq
from datetime import datetime, timedelta

class Task:
    def __init__(self, task_id, name, priority, deadline=None, completed=False):
        self.id = task_id # Contoh: "TO01"
        self.name = name # Nama tugas
        self.priority = priority  # Prioritas (Low=1, Medium=2, High=3, Urgent=4):
        self.deadline = deadline  # Format: "YYYY-MM-DD"
        self.completed = completed # Status selesai/belum

    def __lt__(self, other):
        return self.priority > other.priority  # Untuk max-heap

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.counter = 1
        self.history = HistoryManager()
        self.reminders = ReminderList()

    def add_task(self, name, priority):
        task_id = f"TO{self.counter:02d}"
        new_task = Task(task_id, name, priority)
        heapq.heappush(self.tasks, new_task)
        self.counter += 1
        self.history.record_operation("ADD", new_task)
        return task_id

    def view_tasks(self):
        sorted_tasks = sorted(self.tasks, key=lambda x: -x.priority)
        priority_names = {1: "LOW", 2: "MEDIUM", 3: "HIGH", 4: "URGENT"}
        
        if not sorted_tasks:
            print("Tidak ada tugas.")
            return
            
        print("\n=== DAFTAR TUGAS ===")
        for task in sorted_tasks:
            status = "[Selesai]" if task.completed else "[Belum Selesai]"
            deadline_info = f" | Deadline: {task.deadline}" if task.deadline else ""
            print(f"[{priority_names[task.priority]}] {task.id}: {task.name} [{status}]{deadline_info}")

    def mark_completed(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                old_task = Task(task.id, task.name, task.priority, task.deadline, task.completed)
                task.completed = True
                self.history.record_operation("COMPLETE", old_task)
                print(f"Tugas {task_id} ditandai selesai.")
                return
        print(f"Tugas dengan ID {task_id} tidak ditemukan.")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                deleted_task = self.tasks.pop(i)
                heapq.heapify(self.tasks)
                self.history.record_operation("DELETE", deleted_task)
                print(f"Tugas {task_id} dihapus.")
                return
        print(f"Tugas dengan ID {task_id} tidak ditemukan.")

    def set_deadline(self, task_id, deadline):
        for task in self.tasks:
            if task.id == task_id:
                old_task = Task(task.id, task.name, task.priority, task.deadline, task.completed)
                task.deadline = deadline
                self.reminders.add_reminder(task)
                self.history.record_operation("DEADLINE", old_task)
                print(f"Deadline untuk {task_id} diatur ke {deadline}.")
                return
        print(f"Tugas dengan ID {task_id} tidak ditemukan.")

class HistoryManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def record_operation(self, operation, task):
        self.undo_stack.append((operation, task))
        self.redo_stack.clear()

    def undo(self, task_manager):
        if not self.undo_stack:
            print("Tidak ada operasi untuk dibatalkan.")
            return False
            
        operation, task = self.undo_stack.pop()
        
        if operation == "ADD":
            task_manager.delete_task(task.id)
        elif operation == "DELETE":
            heapq.heappush(task_manager.tasks, task)
        elif operation == "COMPLETE":
            for t in task_manager.tasks:
                if t.id == task.id:
                    t.completed = False
                    break
        elif operation == "DEADLINE":
            for t in task_manager.tasks:
                if t.id == task.id:
                    t.deadline = task.deadline
                    break
        
        self.redo_stack.append((operation, task))
        print("Operasi berhasil dibatalkan.")
        return True

    def redo(self, task_manager):
        if not self.redo_stack:
            print("Tidak ada operasi untuk dikembalikan.")
            return False
            
        operation, task = self.redo_stack.pop()
        
        if operation == "ADD":
            heapq.heappush(task_manager.tasks, task)
        elif operation == "DELETE":
            task_manager.delete_task(task.id)
        elif operation == "COMPLETE":
            for t in task_manager.tasks:
                if t.id == task.id:
                    t.completed = True
                    break
        elif operation == "DEADLINE":
            for t in task_manager.tasks:
                if t.id == task.id:
                    t.deadline = task.deadline
                    break
        
        self.undo_stack.append((operation, task))
        print("Operasi berhasil dikembalikan.")
        return True

class ReminderList:
    def __init__(self):
        self.head = None

    def add_reminder(self, task):
        if not task.deadline:
            return
            
        new_node = ReminderNode(task)
        if not self.head or task.deadline < self.head.task.deadline:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and task.deadline >= current.next.task.deadline:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def view_upcoming(self, days=3):
        upcoming = []
        current = self.head
        today = datetime.now().date()
        
        while current:
            try:
                deadline_date = datetime.strptime(current.task.deadline, "%Y-%m-%d").date()
                if (deadline_date - today).days <= days:
                    upcoming.append(current.task)
                current = current.next
            except:
                current = current.next
                
        if not upcoming:
            print("Tidak ada tugas dengan deadline dalam 3 hari.")
        else:
            print("\n=== TUGAS MENDEKATI DEADLINE ===")
            for task in upcoming:
                deadline_date = datetime.strptime(task.deadline, "%Y-%m-%d").date()
                days_left = (deadline_date - today).days
                print(f"{task.id}: {task.name} - Deadline: {task.deadline} ({days_left} hari lagi)")

class ReminderNode:
    def __init__(self, task, next_node=None):
        self.task = task
        self.next = next_node

def main():
    manager = TaskManager()
    
    while True:
        print("\n=== TASKMASTER PRO ===")
        print("1. Tambah Tugas Baru")
        print("2. Lihat Semua Tugas")
        print("3. Tandai Selesai")
        print("4. Hapus Tugas")
        print("5. Undo Operasi")
        print("6. Redo Operasi")
        print("7. Lihat Reminder")
        print("8. Set Deadline")
        print("9. Keluar")
        
        choice = input("> Pilihan: ")
        
        if choice == "1":
            name = input("Nama tugas: ")
            priority = int(input("Prioritas (1-4): "))
            if 1 <= priority <= 4:
                task_id = manager.add_task(name, priority)
                print(f"Tugas berhasil ditambahkan dengan ID: {task_id}")
            else:
                print("Prioritas harus antara 1-4!")
                
        elif choice == "2":
            manager.view_tasks()
            
        elif choice == "3":
            task_id = input("ID tugas yang selesai: ").upper()
            manager.mark_completed(task_id)
            
        elif choice == "4":
            task_id = input("ID tugas yang dihapus: ").upper()
            manager.delete_task(task_id)
            
        elif choice == "5":
            manager.history.undo(manager)
            
        elif choice == "6":
            manager.history.redo(manager)
            
        elif choice == "7":
            manager.reminders.view_upcoming()
            
        elif choice == "8":
            task_id = input("ID tugas: ").upper()
            deadline = input("Deadline (YYYY-MM-DD): ")
            try:
                datetime.strptime(deadline, "%Y-%m-%d")  # Validasi format
                manager.set_deadline(task_id, deadline)
            except ValueError:
                print("Format deadline salah! Gunakan YYYY-MM-DD")
            
        elif choice == "9":
            print("Keluar dari aplikasi...")
            break
            
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
