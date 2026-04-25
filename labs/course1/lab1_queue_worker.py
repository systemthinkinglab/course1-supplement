#!/usr/bin/env python3
# =============================================================================
# Systems Thinking in the AI Era
# https://systemthinkinglab.ai
#
# This code is part of the "Systems Thinking in the AI Era" course series.
# For more information, educational content, and courses, visit:
# https://systemthinkinglab.ai
# =============================================================================

"""
Systems Thinking in the AI Era I: Universal Building Blocks
Lesson 5: Queue + Worker Async Processing Discovery Lab
Interactive Python Application

This application guides students through the complete lab experience,
running experiments and collecting reflections for automated feedback.
Developing system thinking skills that complement AI rather than compete with it.
"""

import time
import sys
import os
import random
import argparse
import threading
from typing import Optional

# Add the repository root to the Python path for imports
# This allows running from: python labs/course1/lab1_queue_worker.py
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, repo_root)

# Import our building blocks
try:
    from building_blocks.building_blocks import Service, Queue, Worker
except ImportError:
    print("Error: Could not import building_blocks module.")
    print("Please run this script from the repository root:")
    print("  cd system-thinking-in-the-ai-era")
    print("  python labs/course1/lab1_queue_worker.py")
    sys.exit(1)


class LabExperience:
    """Interactive lab experience for Lesson 5"""
    
    def __init__(self, student_name: str = "Student"):
        self.student_name = student_name
        self.experiment_times = {}
        
        # Visual elements
        self.separator = "=" * 80
        self.mini_separator = "-" * 40
        
        # Typewriter settings
        self.typewriter_speed = 0.03  # Seconds between characters
        self.fast_typewriter_speed = 0.01  # Faster for less important text
        self.instant_print = False  # Can be set to True to disable typewriter effect
        
        # Thread safety for print statements during simulations
        self.print_lock = threading.Lock()
    
    def typewriter_print(self, text: str, speed: Optional[float] = None, end: str = "\n"):
        """Print text with typewriter effect"""
        if self.instant_print:
            print(text, end=end)
            return
            
        if speed is None:
            speed = self.typewriter_speed
            
        for char in text:
            print(char, end='', flush=True)
            if char not in [' ', '\n', '\t']:  # Don't delay on whitespace
                time.sleep(speed)
        print(end=end)
    
    def direct_print(self, text: str, end: str = "\n"):
        """Print text directly without typewriter effect (thread-safe)"""
        with self.print_lock:
            print(text, end=end)
    
    def print_header(self, text: str, style: str = "main"):
        """Print formatted headers"""
        if style == "main":
            print(f"\n{self.separator}")
            print(f"🎯 {text.upper()}")
            print(self.separator)
        elif style == "sub":
            print(f"\n{self.mini_separator}")
            print(f"▶️  {text}")
            print(self.mini_separator)
        elif style == "experiment":
            print(f"\n{'🧪' * 20}")
            print(f"🧪 EXPERIMENT: {text}")
            print('🧪' * 20)
    
    def print_experiment(self, text: str):
        """Print experiment headers"""
        self.print_header(text, style="experiment")
    
    def print_info(self, text: str, indent: int = 0):
        """Print informational text with typewriter effect"""
        prefix = "  " * indent + "ℹ️ " if indent == 0 else "  " * indent
        lines = text.strip().split('\n')
        for line in lines:
            self.typewriter_print(f"{prefix}{line}")
    
    def print_action(self, text: str):
        """Print action items with fast typewriter effect"""
        self.typewriter_print(f"⚡ {text}", speed=self.fast_typewriter_speed)
    
    def print_result(self, text: str):
        """Print results with typewriter effect"""
        self.typewriter_print(f"✅ {text}")
    
    def print_warning(self, text: str):
        """Print warnings with typewriter effect"""
        self.typewriter_print(f"⚠️  {text}")
    
    def wait_for_enter(self, prompt: str = "Press ENTER to continue..."):
        """Wait for user to press enter"""
        input(f"\n📍 {prompt}")
    
    def ask_yes_no(self, question: str) -> bool:
        """Ask a yes/no question"""
        while True:
            response = input(f"\n❓ {question} (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please answer 'yes' or 'no'")
    
    def ask_multiple_choice(self, question: str, choices: list, responses: list) -> str:
        """Ask a multiple choice question with educational responses"""
        print(f"\n💭 REFLECTION QUESTION:")
        print(f"   {question}")
        print()
        
        # Display choices
        for i, choice in enumerate(choices, 1):
            print(f"   {i}. {choice}")
        
        # Get user choice
        while True:
            try:
                choice_input = input(f"\n❓ Enter your choice (1-{len(choices)}): ").strip()
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print(f"Please enter a valid number between 1 and {len(choices)}")
        
        # Show the corresponding educational response
        selected_choice = choices[choice_num - 1]
        educational_response = responses[choice_num - 1]
        
        print(f"\n✅ You selected: {selected_choice}")
        # Use typewriter effect for educational response
        print("\n🎯 ", end='')
        self.typewriter_print(educational_response)
        
        self.wait_for_enter("Press ENTER to continue...")
        return selected_choice

    # ===================================================================
    # REUSABLE WORK FUNCTIONS
    # These functions represent the actual business logic.
    # They can be executed by Service (blocking) OR Worker (async)!
    # This demonstrates: building blocks change HOW work executes,
    # not WHAT work gets done.
    # ===================================================================

    def process_image_work(self, duration: int = 15) -> dict:
        """The actual work of processing an image - same whether Service or Worker executes it"""
        task_name = "Process Image"
        self.direct_print(f"   🔧 Processing: {task_name}")
        time.sleep(duration)
        self.direct_print(f"   ✅ Completed: {task_name}")
        return {"task": task_name, "status": "completed", "duration": duration}

    def send_email_work(self, duration: int = 20) -> dict:
        """The actual work of sending email - same whether Service or Worker executes it"""
        task_name = "Send Email"
        self.direct_print(f"   🔧 Processing: {task_name}")
        time.sleep(duration)
        self.direct_print(f"   ✅ Completed: {task_name}")
        return {"task": task_name, "status": "completed", "duration": duration}

    def generate_report_work(self, duration: int = 15) -> dict:
        """The actual work of generating a report - same whether Service or Worker executes it"""
        task_name = "Generate Report"
        self.direct_print(f"   🔧 Processing: {task_name}")
        time.sleep(duration)
        self.direct_print(f"   ✅ Completed: {task_name}")
        return {"task": task_name, "status": "completed", "duration": duration}

    def update_database_work(self, duration: int = 10) -> dict:
        """The actual work of updating database - same whether Service or Worker executes it"""
        task_name = "Update Database"
        self.direct_print(f"   🔧 Processing: {task_name}")
        time.sleep(duration)
        self.direct_print(f"   ✅ Completed: {task_name}")
        return {"task": task_name, "status": "completed", "duration": duration}

    def run_welcome(self):
        """Welcome and introduction"""
        self.print_header("WELCOME TO SYSTEMS THINKING IN THE AI ERA")
        # Use regular print for course info
        print("\n🎓 Systems Thinking in the AI Era I: Universal Building Blocks")
        print("📚 Lesson 5: Queue + Worker Async Processing Discovery Lab\n")
        
        # Use typewriter for transformational message
        self.typewriter_print("Transform from a code writer who creates blocking operations")
        self.typewriter_print("to a system thinker who designs responsive, scalable systems!")
        
        self.student_name = input("\n\n👤 What's your name? ").strip() or "Student"
        self.typewriter_print(f"\nWelcome, {self.student_name}! Let's begin your discovery journey.")
        
        self.print_info("""
Today you'll experience firsthand why system thinkers choose Queue + Worker
building blocks over Service building blocks for scalable systems - from Instagram 
photo processing to Netflix video encoding.

You'll run 4 experiments comparing building block patterns:
1. Service Building Block (The Blocking Problem)
2. Queue + Worker Building Blocks (Message-Based Async Processing)
3. Queue Distributing to Multiple Workers (Parallel Processing)
4. Queue + Worker Failure Handling (System Resilience)

After each experiment, you'll reflect on your architectural discoveries.
""")
        
        self.wait_for_enter("Ready to transform your system thinking? Press ENTER to begin!")
    
    def experiment_1_blocking(self):
        """Experiment 1: Service Building Block (Blocking Processing)"""
        self.print_experiment("1 - SERVICE BUILDING BLOCK (BLOCKING PROCESSING)")
        
        self.print_info("""
In this experiment, you'll experience what happens when a Service building block
processes everything synchronously. The Service handles each request completely
before moving to the next one - this is how many code writers first
implement features, and why users get frustrated!
""")
        
        self.wait_for_enter()
        
        # Create Service building block for blocking demonstration
        blocking_service = Service("blocking_api")

        # KEY INSIGHT: Service routes wrap the SAME work functions that Workers will use!
        # The work is identical - only the execution pattern (blocking vs async) differs.

        @blocking_service.route("/process_image")
        def process_image_handler():
            self.direct_print(f"⏳ Service executing: /process_image (UI FROZEN while waiting...)")
            result = self.process_image_work(duration=15)  # Same work function Workers will use!
            self.direct_print(f"✅ Service completed: {result['task']} after {result['duration']}s")
            return result

        @blocking_service.route("/send_email")
        def send_email_handler():
            self.direct_print(f"⏳ Service executing: /send_email (UI FROZEN while waiting...)")
            result = self.send_email_work(duration=20)  # Same work function Workers will use!
            self.direct_print(f"✅ Service completed: {result['task']} after {result['duration']}s")
            return result

        @blocking_service.route("/generate_report")
        def generate_report_handler():
            self.direct_print(f"⏳ Service executing: /generate_report (UI FROZEN while waiting...)")
            result = self.generate_report_work(duration=15)  # Same work function Workers will use!
            self.direct_print(f"✅ Service completed: {result['task']} after {result['duration']}s")
            return result

        @blocking_service.route("/update_database")
        def update_database_handler():
            self.direct_print(f"⏳ Service executing: /update_database (UI FROZEN while waiting...)")
            result = self.update_database_work(duration=10)  # Same work function Workers will use!
            self.direct_print(f"✅ Service completed: {result['task']} after {result['duration']}s")
            return result
        
        # Service endpoints to call
        endpoints = [
            "/process_image",
            "/send_email", 
            "/generate_report",
            "/update_database"
        ]
        
        self.typewriter_print("\n🚀 Starting Service building block processing...")
        self.typewriter_print("Notice how each request BLOCKS until completion!\n")
        
        start_time = time.time()
        
        for endpoint in endpoints:
            self.typewriter_print(f"📤 User clicks: {endpoint}", speed=self.fast_typewriter_speed)
            self.typewriter_print("   (User must wait... cannot do anything else!)")
            
            # Service processes request synchronously (blocking)
            response = blocking_service.handle_request(endpoint)
            
            if response["status"] == 200:
                self.typewriter_print(f"   📥 Service response: {response['data']['task']} completed", speed=self.fast_typewriter_speed)
            else:
                self.typewriter_print(f"   ❌ Service error: {response['error']}", speed=self.fast_typewriter_speed)
            print()
        
        total_time = time.time() - start_time
        self.experiment_times['experiment_1'] = total_time
        
        # Show Service statistics
        service_stats = blocking_service.get_stats()
        print(f"📊 Service Building Block Statistics:")
        print(f"   🔧 Requests processed: {service_stats['requests']}")
        print(f"   ⏱️  Average response time: {service_stats['avg_response_time']:.1f}s")
        print(f"   ⏱️  Max response time: {service_stats['max_response_time']:.1f}s")
        
        self.print_result(f"Service completed all {len(endpoints)} requests in {total_time:.1f} seconds")
        self.print_warning("But the UI was completely BLOCKED during each request!")
        self.print_warning("Users couldn't click anything while Service was processing!")
        
        # Multiple choice reflections for Experiment 1
        self.print_header("EXPERIMENT 1 REFLECTIONS", style="sub")
        
        # Question 1
        self.ask_multiple_choice(
            "What was the most frustrating aspect of the Service building block's blocking behavior?",
            [
                "I had to wait for each request to complete before doing anything else",
                "The processing times were too long",
                "The system wasn't reliable enough"
            ],
            [
                "Exactly! This is the core problem with blocking operations - they freeze the entire user interface. System thinkers recognize this and choose async patterns like Queue + Worker to keep systems responsive.",
                "Great observation! While processing time matters, the real issue is that users can't do ANYTHING else while waiting. Even fast operations become problematic when they block the UI completely.",
                "Good thinking about reliability! However, the Service building block actually worked perfectly - the frustration comes from being unable to multitask. This is why async patterns are crucial for user experience."
            ]
        )
        
        # Question 2
        self.ask_multiple_choice(
            "In a real application, what would happen if users experienced this blocking behavior?",
            [
                "Users would think the application crashed and try to refresh or restart",
                "Users would be patient and wait for each operation to complete",
                "Users would find workarounds to avoid the blocking operations"
            ],
            [
                "Absolutely correct! This is exactly what happens in production. Users interpret frozen UIs as crashes, leading to support tickets, bad reviews, and user churn. This is why AI-empowered system thinkers prioritize responsive architectures - understanding interface patterns that AI cannot design.",
                "Unfortunately, users rarely have this patience in practice. Modern users expect instant feedback and the ability to multitask. Blocking UIs feel broken to users, even when they're working correctly.",
                "Smart thinking! Some power users do find workarounds, but most users simply abandon applications that feel unresponsive. The better solution is to fix the architecture with async patterns."
            ]
        )
        
        # Question 3
        self.ask_multiple_choice(
            "What's the fundamental architectural problem with the Service building block approach?",
            [
                "Service building blocks are inherently slow",
                "The Service handles both user interface AND long-running processing in the same thread",
                "Service building blocks don't have enough error handling"
            ],
            [
                "Not quite! Service building blocks can be very fast for quick operations. The problem isn't speed - it's that ANY processing time blocks the user interface when everything runs synchronously.",
                "Perfect analysis! You've identified the core architectural issue. Mixing UI responsiveness with long-running tasks in the same execution thread is the fundamental flaw. This is exactly why Queue + Worker patterns separate these concerns.",
                "Good systems thinking! While error handling is important, the blocking behavior would still be problematic even with perfect error handling. The real issue is the synchronous execution model."
            ]
        )
        
        if self.ask_yes_no("Ready to see how Queue + Worker building blocks solve this problem?"):
            self.experiment_2_async()
    
    def experiment_2_async(self):
        """Experiment 2: Queue + Worker Solution"""
        self.print_experiment("2 - QUEUE + WORKER SOLUTION (ASYNC)")
        
        self.print_info("""
Now let's see how the Queue + Worker building block pattern transforms
the user experience. The Queue building block will handle message routing,
while the Worker building block processes tasks in the background.
""")

        self.print_header("KEY INSIGHT: Same Work, Different Execution Pattern", style="sub")
        self.print_info("""
Watch carefully: The Worker will execute the EXACT SAME work functions
that the Service just executed (process_image_work, send_email_work, etc.).

The business logic is IDENTICAL. What changes is HOW and WHEN it executes:
• Service: Executes work immediately, blocks until complete
• Worker: Executes work in background, never blocks user interface

This separation of work (what) from execution pattern (how) is the essence
of system thinking!
""")

        self.wait_for_enter()
        
        # Create Queue + Worker system
        task_queue = Queue("task_queue")
        worker = Worker("async_worker")
        
        # KEY INSIGHT: Worker uses the SAME work functions that Service used!
        # The work is identical - only the execution pattern differs (async vs blocking).

        # Register individual job types on Worker - same structure as Service routes!
        def process_image_task(data):
            """Worker task that calls the same work function Service used"""
            return self.process_image_work(duration=data['duration'])

        def send_email_task(data):
            """Worker task that calls the same work function Service used"""
            return self.send_email_work(duration=data['duration'])

        def generate_report_task(data):
            """Worker task that calls the same work function Service used"""
            return self.generate_report_work(duration=data['duration'])

        def update_database_task(data):
            """Worker task that calls the same work function Service used"""
            return self.update_database_work(duration=data['duration'])

        # Register each job type - parallel structure to Service routes!
        worker.register_job_type("process_image", process_image_task)
        worker.register_job_type("send_email", send_email_task)
        worker.register_job_type("generate_report", generate_report_task)
        worker.register_job_type("update_database", update_database_task)

        # Register Queue subscribers for each task type
        @task_queue.subscriber("process_image")
        def queue_process_image_handler(message):
            self.direct_print(f"   📬 Queue dispatching: Process Image to Worker")
            job_id = worker.submit_job("process_image", message)
            return {"status": "queued", "job_id": job_id}

        @task_queue.subscriber("send_email")
        def queue_send_email_handler(message):
            self.direct_print(f"   📬 Queue dispatching: Send Email to Worker")
            job_id = worker.submit_job("send_email", message)
            return {"status": "queued", "job_id": job_id}

        @task_queue.subscriber("generate_report")
        def queue_generate_report_handler(message):
            self.direct_print(f"   📬 Queue dispatching: Generate Report to Worker")
            job_id = worker.submit_job("generate_report", message)
            return {"status": "queued", "job_id": job_id}

        @task_queue.subscriber("update_database")
        def queue_update_database_handler(message):
            self.direct_print(f"   📬 Queue dispatching: Update Database to Worker")
            job_id = worker.submit_job("update_database", message)
            return {"status": "queued", "job_id": job_id}
        
        # Start worker
        worker.start()
        
        # Submit tasks to Queue (same durations as Service for fair comparison)
        # Each task has its own message type - parallel structure to Service endpoints!
        tasks = [
            ("Process Image", "process_image", 15),
            ("Send Email", "send_email", 20),
            ("Generate Report", "generate_report", 15),
            ("Update Database", "update_database", 10)
        ]

        self.typewriter_print("\n🚀 Starting Queue + Worker async system...")
        self.typewriter_print("Notice how the Queue building block handles message routing!\n")

        start_time = time.time()

        for task_name, message_type, duration in tasks:
            self.typewriter_print(f"📤 Submitting to Queue: {task_name}", speed=self.fast_typewriter_speed)
            # Enqueue message - Queue automatically dispatches to correct subscriber
            success = task_queue.enqueue({
                "duration": duration
            }, message_type=message_type)  # Each task type has its own Queue subscriber!

            if success:
                self.typewriter_print(f"✅ Message queued: {task_name}", speed=self.fast_typewriter_speed)
                self.typewriter_print("   (Queue will automatically dispatch to Worker!)\n")
            else:
                self.typewriter_print(f"❌ Failed to queue: {task_name}\n", speed=self.fast_typewriter_speed)

            time.sleep(0.5)  # Simulate user doing other actions
        
        self.typewriter_print("🎯 All messages submitted to Queue! Auto-dispatching to Worker...\n")
        
        # Wait for processing to complete with active monitoring
        expected_jobs = len(tasks)
        self.print_info(f"⏳ Monitoring Queue + Worker progress: waiting for {expected_jobs} tasks...")
        
        max_wait_time = 90  # Maximum wait time
        check_interval = 2  # Check every 2 seconds
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            worker_stats = worker.get_stats()
            total_processed = worker_stats['completed_jobs'] + worker_stats['failed_jobs']
            
            self.direct_print(f"   📊 Progress: {total_processed}/{expected_jobs} tasks processed ({worker_stats['completed_jobs']} completed)")
            
            if total_processed >= expected_jobs:
                self.direct_print(f"   ✅ All {expected_jobs} tasks processed! Continuing...")
                break
                
            time.sleep(check_interval)
            elapsed_time += check_interval
        
        if elapsed_time >= max_wait_time:
            self.print_warning(f"Timeout reached after {max_wait_time}s - continuing with current results")
        
        total_time = time.time() - start_time
        self.experiment_times['experiment_2'] = total_time
        
        # Show Queue statistics
        queue_stats = task_queue.get_stats()
        print(f"\n📊 Queue Statistics:")
        print(f"   📬 Messages processed: {queue_stats['total_processed']}")
        print(f"   📬 Success rate: {queue_stats['success_rate']:.1%}")
        print(f"   📬 Active subscribers: {queue_stats['active_subscribers']}")
        
        # Show Worker statistics  
        worker_stats = worker.get_stats()
        print(f"\n📊 Worker Statistics:")
        print(f"   🔧 Jobs completed: {worker_stats['completed_jobs']}")
        print(f"   🔧 Success rate: {worker_stats['success_rate']:.1%}")
        print(f"   🔧 Total jobs processed: {worker_stats['total_jobs']}")
        
        # Cleanup
        worker.stop()
        task_queue.stop()
        
        self.print_result(f"Queue + Worker completed all tasks in {total_time:.1f} seconds")
        self.print_info("Queue + Worker building blocks created responsive system - UI never blocked!")
        
        # Multiple choice reflections for Experiment 2
        self.print_header("EXPERIMENT 2 REFLECTIONS", style="sub")
        
        # Question 1
        self.ask_multiple_choice(
            "What was the key difference in user experience between Service and Queue + Worker?",
            [
                "Queue + Worker was faster at processing tasks",
                "Queue + Worker allowed immediate responses while processing happened in background",
                "Queue + Worker had better error messages"
            ],
            [
                "Good observation about performance! But the real breakthrough isn't speed - it's responsiveness. Even if Queue + Worker took the same time, the immediate responses and background processing create a dramatically better user experience.",
                "Excellent! You've grasped the fundamental architectural advantage. The Queue building block provides immediate acceptance of requests, while Worker building blocks handle processing asynchronously. This separation is what makes modern applications feel responsive.",
                "Error handling is important, but that's not the main difference here. The game-changer is that users get instant feedback and can continue working while processing happens behind the scenes."
            ]
        )
        
        # Question 2
        self.ask_multiple_choice(
            "What role does the Queue building block play in this architecture?",
            [
                "It speeds up the processing of individual tasks",
                "It acts as a reliable buffer between user requests and background processing",
                "It reduces the amount of memory needed by the system"
            ],
            [
                "Not exactly! The Queue doesn't make individual tasks faster - the Worker still takes the same time to process each task. The Queue's value is in handling the coordination and persistence of work.",
                "Perfect understanding! The Queue building block is like a reliable inbox that accepts messages instantly and ensures they reach the Worker. This buffering allows immediate user responses while guaranteeing work gets done.",
                "Memory optimization isn't the Queue's primary role here. Its real value is providing reliable message persistence and routing between user-facing components and background Workers."
            ]
        )
        
        # Question 3
        self.ask_multiple_choice(
            "Why is this Queue + Worker pattern used by companies like Instagram and Netflix?",
            [
                "Because they process millions of tasks and need the reliability and scalability",
                "Because it's easier to implement than Service building blocks",
                "Because it uses less server resources"
            ],
            [
                "Exactly right! At scale, reliability and responsiveness become critical. When Instagram processes millions of photo uploads, they can't have users waiting with frozen screens. Queue + Worker ensures instant user feedback and reliable background processing.",
                "Actually, Queue + Worker is more complex to implement than simple Service calls! Companies choose this pattern despite the complexity because the user experience and scalability benefits are worth it.",
                "Resource usage isn't the primary driver. The pattern is chosen for user experience and reliability. While it can be more efficient at scale, the main benefits are responsiveness and fault tolerance."
            ]
        )
        
        if self.ask_yes_no("Ready to see how Queue + Worker scales with multiple Workers?"):
            self.experiment_3_parallel()
    
    def experiment_3_parallel(self):
        """Experiment 3: Single Worker vs Multiple Workers with Queue Distribution"""
        self.print_experiment("3 - QUEUE DISTRIBUTING TO MULTIPLE WORKERS (PARALLEL PROCESSING)")
        
        self.print_info("""
Now let's experience the power of horizontal scaling with Queue + Worker patterns! 
We'll run the SAME tasks twice:
1. First with Queue → 1 Worker (sequential processing)
2. Then with Queue → 3 Workers (parallel processing)

The Queue building block will intelligently distribute work!
""")
        
        self.wait_for_enter()
        
        # Define the tasks we'll use for both runs (realistic processing times)
        # Multiple instances of each work type to demonstrate parallel processing
        tasks = [
            ("Image 1", "process_image", 10), ("Image 2", "process_image", 12), ("Image 3", "process_image", 8),
            ("Email 1", "send_email", 15), ("Email 2", "send_email", 18), ("Email 3", "send_email", 12),
            ("Report 1", "generate_report", 20), ("Report 2", "generate_report", 25), ("Report 3", "generate_report", 15)
        ]
        
        # ===== PART 1: Queue + Single Worker =====
        self.print_header("PART 1: Queue + Single Worker (Sequential Processing)", style="sub")
        self.print_info("Watch how the Queue routes all tasks to one Worker...")
        
        # Create Queue + single worker system
        single_queue = Queue("single_queue")
        single_worker = Worker("single_worker")

        # Register the SAME work functions on single Worker
        def process_image_single(data):
            """Single Worker executing the same work function"""
            task_id = data.get('task_id', '')
            self.direct_print(f"   🔧 Single Worker processing: {task_id}")
            result = self.process_image_work(duration=data['duration'])
            return result

        def send_email_single(data):
            """Single Worker executing the same work function"""
            task_id = data.get('task_id', '')
            self.direct_print(f"   🔧 Single Worker processing: {task_id}")
            result = self.send_email_work(duration=data['duration'])
            return result

        def generate_report_single(data):
            """Single Worker executing the same work function"""
            task_id = data.get('task_id', '')
            self.direct_print(f"   🔧 Single Worker processing: {task_id}")
            result = self.generate_report_work(duration=data['duration'])
            return result

        # Register job types on single Worker
        single_worker.register_job_type("process_image", process_image_single)
        single_worker.register_job_type("send_email", send_email_single)
        single_worker.register_job_type("generate_report", generate_report_single)

        # Register Queue subscribers for each job type
        @single_queue.subscriber("process_image")
        def single_queue_image_handler(message):
            task_id = message.get('task_id', '')
            self.direct_print(f"   📬 Queue routing to single Worker: {task_id}")
            job_id = single_worker.submit_job("process_image", message)
            return {"status": "queued", "job_id": job_id}

        @single_queue.subscriber("send_email")
        def single_queue_email_handler(message):
            task_id = message.get('task_id', '')
            self.direct_print(f"   📬 Queue routing to single Worker: {task_id}")
            job_id = single_worker.submit_job("send_email", message)
            return {"status": "queued", "job_id": job_id}

        @single_queue.subscriber("generate_report")
        def single_queue_report_handler(message):
            task_id = message.get('task_id', '')
            self.direct_print(f"   📬 Queue routing to single Worker: {task_id}")
            job_id = single_worker.submit_job("generate_report", message)
            return {"status": "queued", "job_id": job_id}

        single_worker.start()
        
        print("\n🚀 Starting Queue + single Worker processing...")
        print("⏳ Queue will route tasks ONE AT A TIME to single Worker...\n")
        
        start_time_single = time.time()

        # Submit all tasks to Queue with proper message types
        for task_name, job_type, duration in tasks:
            single_queue.enqueue({
                "task_id": task_name,
                "duration": duration
            }, message_type=job_type)  # Route to correct job type!
            self.direct_print(f"📤 Queued: {task_name}")
        
        self.direct_print(f"\n🎯 All {len(tasks)} tasks queued!")
        self.direct_print("⏳ Queue dispatching sequentially to single Worker...\n")
        
        # Wait for processing to complete
        # Active monitoring for single worker
        expected_jobs = len(tasks)
        self.print_info(f"⏳ Monitoring progress: waiting for {expected_jobs} sequential tasks...")
        
        max_wait_time = 180  # Maximum wait time for sequential processing
        check_interval = 3   # Check every 3 seconds for sequential
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            worker_stats = single_worker.get_stats()
            total_processed = worker_stats['completed_jobs'] + worker_stats['failed_jobs']
            
            self.direct_print(f"   📊 Progress: {total_processed}/{expected_jobs} tasks processed")
            
            if total_processed >= expected_jobs:
                self.direct_print(f"   ✅ All {expected_jobs} tasks processed! Continuing...")
                break
                
            time.sleep(check_interval)
            elapsed_time += check_interval
        
        if elapsed_time >= max_wait_time:
            self.print_warning(f"Timeout reached after {max_wait_time}s - continuing with current results")
        
        single_time = time.time() - start_time_single
        
        # Show single worker stats
        single_stats = single_worker.get_stats()
        single_queue_stats = single_queue.get_stats()
        
        single_worker.stop()
        single_queue.stop()
        
        self.print_result(f"Queue + Single Worker completed {len(tasks)} tasks in {single_time:.1f} seconds")
        print(f"   📬 Queue processed: {single_queue_stats['total_processed']} messages")
        print(f"   🔧 Worker completed: {single_stats['completed_jobs']} jobs")
        self.print_info("That felt slow... Now let's see the Queue distribute to multiple Workers!")
        
        self.wait_for_enter("Press ENTER to run with Queue + 3 Workers...")
        
        # ===== PART 2: Queue + Multiple Workers =====
        self.print_header("PART 2: Queue + Multiple Workers (Parallel Processing)", style="sub")
        self.print_info("Watch how the Queue intelligently distributes to multiple Workers!")
        
        # Create Queue + multiple workers system
        multi_queue = Queue("multi_queue")
        workers = []

        # Create 3 workers
        for i in range(3):
            worker = Worker(f"worker_{i+1}")
            workers.append(worker)

        # KEY INSIGHT: Register the SAME work functions on ALL workers!
        # Each Worker can execute process_image, send_email, generate_report
        # The Queue will distribute work across them intelligently.
        def make_work_handlers(worker_id):
            """Create work handlers for each Worker that use the same work functions"""
            def process_image_multi(data):
                task_id = data.get('task_id', '')
                self.direct_print(f"   🔧 Worker {worker_id} processing: {task_id}")
                result = self.process_image_work(duration=data['duration'])
                return result

            def send_email_multi(data):
                task_id = data.get('task_id', '')
                self.direct_print(f"   🔧 Worker {worker_id} processing: {task_id}")
                result = self.send_email_work(duration=data['duration'])
                return result

            def generate_report_multi(data):
                task_id = data.get('task_id', '')
                self.direct_print(f"   🔧 Worker {worker_id} processing: {task_id}")
                result = self.generate_report_work(duration=data['duration'])
                return result

            return process_image_multi, send_email_multi, generate_report_multi

        # Register all job types on all Workers
        for i, worker in enumerate(workers, 1):
            process_image_handler, send_email_handler, generate_report_handler = make_work_handlers(i)
            worker.register_job_type("process_image", process_image_handler)
            worker.register_job_type("send_email", send_email_handler)
            worker.register_job_type("generate_report", generate_report_handler)
            worker.start()

        # Register Queue subscribers that distribute to multiple workers
        @multi_queue.subscriber("process_image")
        def multi_queue_image_handler(message):
            task_id = message.get('task_id', '')
            # Choose worker with least load (random for simplicity)
            worker = random.choice(workers)
            self.direct_print(f"   📬 Queue distributing to {worker.name}: {task_id}")
            job_id = worker.submit_job("process_image", message)
            return {"status": "distributed", "worker": worker.name, "job_id": job_id}

        @multi_queue.subscriber("send_email")
        def multi_queue_email_handler(message):
            task_id = message.get('task_id', '')
            worker = random.choice(workers)
            self.direct_print(f"   📬 Queue distributing to {worker.name}: {task_id}")
            job_id = worker.submit_job("send_email", message)
            return {"status": "distributed", "worker": worker.name, "job_id": job_id}

        @multi_queue.subscriber("generate_report")
        def multi_queue_report_handler(message):
            task_id = message.get('task_id', '')
            worker = random.choice(workers)
            self.direct_print(f"   📬 Queue distributing to {worker.name}: {task_id}")
            job_id = worker.submit_job("generate_report", message)
            return {"status": "distributed", "worker": worker.name, "job_id": job_id}
        
        print("\n🚀 Starting Queue + 3 Workers processing...")
        print("⚡ Queue will intelligently distribute tasks SIMULTANEOUSLY!\n")
        
        start_time_parallel = time.time()

        # Submit all tasks to Queue with proper message types
        for task_name, job_type, duration in tasks:
            multi_queue.enqueue({
                "task_id": task_name,
                "duration": duration
            }, message_type=job_type)  # Route to correct job type!
            self.direct_print(f"📤 Queued: {task_name}")
        
        self.direct_print(f"\n🎯 All {len(tasks)} tasks queued!")
        self.direct_print("⚡ Queue distributing in PARALLEL to 3 Workers...\n")
        
        # Wait for parallel processing to complete
        # Active monitoring instead of fixed wait time
        expected_jobs = len(tasks)
        self.print_info(f"⏳ Monitoring progress: waiting for {expected_jobs} tasks to complete...")
        
        max_wait_time = 120  # Maximum wait time to prevent infinite hanging
        check_interval = 2   # Check every 2 seconds
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            total_completed = sum(worker.get_stats()['completed_jobs'] for worker in workers)
            total_failed = sum(worker.get_stats()['failed_jobs'] for worker in workers)
            total_processed = total_completed + total_failed
            
            self.direct_print(f"   📊 Progress: {total_processed}/{expected_jobs} tasks processed ({total_completed} completed)")
            
            if total_processed >= expected_jobs:
                self.direct_print(f"   ✅ All {expected_jobs} tasks processed! Continuing...")
                break
                
            time.sleep(check_interval)
            elapsed_time += check_interval
        
        if elapsed_time >= max_wait_time:
            self.print_warning(f"Timeout reached after {max_wait_time}s - continuing with current results")
        
        parallel_time = time.time() - start_time_parallel
        
        # Show multi-worker stats
        multi_queue_stats = multi_queue.get_stats()
        total_worker_jobs = sum(worker.get_stats()['completed_jobs'] for worker in workers)
        
        # Stop all workers and queue
        for worker in workers:
            worker.stop()
        multi_queue.stop()
        
        # Store total experiment time (both parts)
        total_experiment_time = single_time + parallel_time
        self.experiment_times['experiment_3'] = total_experiment_time
        
        # Show dramatic comparison
        print(f"\n{'🎯' * 40}")
        print("🎯 QUEUE + WORKER SCALING COMPARISON")
        print(f"{'🎯' * 40}")
        self.print_result(f"Queue + 1 Worker:  {single_time:.1f} seconds (sequential)")
        self.print_result(f"Queue + 3 Workers: {parallel_time:.1f} seconds (parallel)")
        speedup = single_time / parallel_time if parallel_time > 0 else 0
        self.print_result(f"Speedup:           {speedup:.1f}x faster with Queue distribution!")
        
        print(f"\n📊 Queue Distribution Statistics:")
        print(f"   📬 Single Queue processed: {single_queue_stats['total_processed']} → 1 Worker")
        print(f"   📬 Multi Queue processed: {multi_queue_stats['total_processed']} → 3 Workers")
        print(f"   🔧 Total Worker jobs: {total_worker_jobs} (distributed across 3 Workers)")
        
        self.print_info(f"""
🚀 Queue + Worker vs Service Building Block Scaling:
   • Service building block: Sequential processing, blocking behavior
   • Queue + Worker building blocks: Parallel processing, non-blocking
   • Queue intelligently distributed {len(tasks)} tasks across 3 Workers
   • {speedup:.1f}x performance improvement over Service-only approach
   • Queue handled load balancing automatically
   • Instagram: Uses Queue + Worker instead of Service for photo processing
   • Netflix: Uses Queue + Worker instead of Service for video encoding
""")
        
        # Multiple choice reflections for Experiment 3
        self.print_header("EXPERIMENT 3 REFLECTIONS", style="sub")
        
        # Question 1
        self.ask_multiple_choice(
            f"You experienced {speedup:.1f}x speedup with 3 Workers vs 1 Worker. What does this teach you about scaling?",
            [
                "Adding more Workers always gives linear performance improvements",
                "Parallel processing can dramatically improve throughput for the same work",
                "The Queue building block is the bottleneck that limits scaling"
            ],
            [
                "Great intuition, but scaling isn't always perfectly linear! There are limits due to coordination overhead, resource contention, and the nature of the work. However, you're right that adding Workers often provides significant improvements.",
                "Excellent insight! This is the power of horizontal scaling. Instead of making one Worker faster (vertical scaling), we add more Workers (horizontal scaling). This approach is how companies like Netflix handle millions of video encoding tasks simultaneously.",
                "Actually, the Queue handled the distribution beautifully! The Queue building block is designed for this exact scenario - coordinating work across multiple Workers. The bottleneck is more likely to be the Workers themselves or external resources."
            ]
        )
        
        # Question 2
        self.ask_multiple_choice(
            "What was the Queue building block's role in enabling parallel processing?",
            [
                "It made each individual Worker process tasks faster",
                "It intelligently distributed tasks across multiple Workers automatically",
                "It reduced the memory usage of each Worker"
            ],
            [
                "Not quite! The Queue doesn't change how fast each Worker processes individual tasks. Each Worker still takes the same time per task. The magic is in the distribution and coordination.",
                "Perfect! The Queue building block acted as an intelligent load balancer, automatically routing tasks to available Workers. This automatic distribution is what makes the pattern so powerful - you just add more Workers and the Queue handles the coordination.",
                "Memory optimization isn't the Queue's primary function here. Its real value is in coordinating work distribution and ensuring no tasks are lost, even with multiple Workers running in parallel."
            ]
        )
        
        # Question 3
        self.ask_multiple_choice(
            "If you had 10 Workers instead of 3, what would likely happen?",
            [
                "You'd get exactly 10/3 = 3.33x better performance",
                "Performance would improve significantly but might hit other bottlenecks",
                "The system would become unstable with too many Workers"
            ],
            [
                "Linear scaling would be ideal, but real systems rarely achieve perfect linearity! As you add more Workers, you might hit bottlenecks like database connections, network bandwidth, or external service limits.",
                "Excellent systems thinking! You understand that scaling has limits. With 10 Workers, you'd likely see great improvement until you hit bottlenecks elsewhere in the system. This is why system thinkers think holistically about architecture - considering constraints that AI cannot anticipate.",
                "Well-designed Queue + Worker systems are quite stable with many Workers! The Queue building block handles coordination gracefully. The limitation is usually external resources, not the Workers themselves."
            ]
        )
        
        if self.ask_yes_no("Ready for the final experiment on failure handling?"):
            self.experiment_4_resilience()
    
    def experiment_4_resilience(self):
        """Experiment 4: Queue + Worker Failure Handling"""
        self.print_experiment("4 - QUEUE + WORKER FAILURE HANDLING (SYSTEM RESILIENCE)")
        
        self.print_info("""
Real systems face failures - APIs timeout, services crash, networks fail.
Let's see how the Queue + Worker pattern provides fault isolation and
message persistence, ensuring one user's problem doesn't crash the system
for everyone else.
""")

        self.wait_for_enter("Press ENTER to continue...")
        
        # Create resilient Queue + Worker system
        resilient_queue = Queue("resilient_queue")
        resilient_worker = Worker("resilient_worker")
        
        # Track processing results for demonstration
        processing_results = []
        
        # Register Queue subscriber that handles failures gracefully
        @resilient_queue.subscriber("risky_task")
        def resilient_queue_handler(message):
            task_name = message['name']
            self.direct_print(f"   📬 Queue routing risky task to Worker: {task_name}")
            try:
                job_id = resilient_worker.submit_job("risky_task", message)
                return {"status": "queued", "job_id": job_id, "task": task_name}
            except Exception as e:
                self.direct_print(f"   📬 Queue caught Worker submission error for {task_name}: {e}")
                processing_results.append({"task": task_name, "status": "queue_failed", "error": str(e)})
                return {"status": "failed_to_queue", "error": str(e)}
        
        # Worker that sometimes fails (with realistic processing times)
        def risky_task(data):
            task_name = data['name']
            task_index = data.get('index', 0)
            fail_chance = data.get('fail_chance', 0.3)
            duration = data.get('duration', 8)  # Realistic processing time
            
            self.direct_print(f"   🔧 Worker processing: {task_name}")
            time.sleep(duration)
            
            # Ensure some tasks definitely fail for educational purposes
            # Tasks 3, 7, and 10 will always fail, others use random chance
            force_fail = task_index in [3, 7, 10]
            
            if force_fail or (not force_fail and random.random() < fail_chance):
                error_msg = f"Task {task_name} failed (simulating API timeout/crash)!"
                self.direct_print(f"   ❌ Worker FAILED: {task_name} - {error_msg}")
                processing_results.append({"task": task_name, "status": "failed", "error": error_msg})
                raise Exception(error_msg)
            else:
                self.direct_print(f"   ✅ Worker completed: {task_name}")
                processing_results.append({"task": task_name, "status": "completed"})
                return {"status": "completed", "task": task_name}
        
        resilient_worker.register_job_type("risky_task", risky_task)
        
        # Start worker
        resilient_worker.start()
        
        # Submit tasks with failure possibility
        tasks = [f"UserTask_{i+1}" for i in range(12)]
        
        print("\n🚀 Starting Queue + Worker resilient system test...")
        print("Some tasks will fail (30% chance) - watch how the system handles it!\n")
        
        start_time = time.time()
        
        # Submit all tasks to Queue
        for i, task_name in enumerate(tasks, 1):
            self.direct_print(f"📤 User submitting to Queue: {task_name}")
            success = resilient_queue.enqueue({
                "name": task_name,
                "index": i,
                "fail_chance": 0.3,
                "duration": 8  # Realistic processing time
            }, message_type="risky_task")
            
            if success:
                self.direct_print(f"✅ Queued: {task_name} (Queue provides persistence)")
            else:
                self.direct_print(f"❌ Queue full: {task_name}")
                processing_results.append({"task": task_name, "status": "queue_full"})
            self.direct_print("")
        
        self.direct_print(f"🎯 All {len(tasks)} tasks submitted to Queue!")
        self.direct_print("📬 Queue automatically dispatching to Worker with failure handling...\n")
        
        # Wait for processing to complete with active monitoring
        expected_jobs = len(tasks)
        self.print_info(f"⏳ Monitoring resilient processing: waiting for {expected_jobs} tasks...")
        
        max_wait_time = 120  # Maximum wait time
        check_interval = 2   # Check every 2 seconds
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            worker_stats = resilient_worker.get_stats()
            total_processed = worker_stats['completed_jobs'] + worker_stats['failed_jobs']
            
            self.direct_print(f"   📊 Progress: {total_processed}/{expected_jobs} tasks processed ({worker_stats['completed_jobs']} completed, {worker_stats['failed_jobs']} failed)")
            
            if total_processed >= expected_jobs:
                self.direct_print(f"   ✅ All {expected_jobs} tasks processed! Continuing...")
                break
                
            time.sleep(check_interval)
            elapsed_time += check_interval
        
        if elapsed_time >= max_wait_time:
            self.print_warning(f"Timeout reached after {max_wait_time}s - continuing with current results")
        
        total_time = time.time() - start_time
        self.experiment_times['experiment_4'] = total_time
        
        # Analyze results
        succeeded = len([r for r in processing_results if r["status"] == "completed"])
        failed = len([r for r in processing_results if r["status"] == "failed"])
        
        # Show comprehensive statistics
        queue_stats = resilient_queue.get_stats()
        worker_stats = resilient_worker.get_stats()
        
        print(f"\n{'📊' * 40}")
        print("📊 QUEUE + WORKER RESILIENCE ANALYSIS")
        print(f"{'📊' * 40}")
        
        print(f"\n📬 Queue Performance:")
        print(f"   Messages processed: {queue_stats['total_processed']}")
        print(f"   Success rate: {queue_stats['success_rate']:.1%}")
        print(f"   Failed dispatches: {queue_stats['total_failed']}")
        
        print(f"\n🔧 Worker Performance:")
        print(f"   Jobs completed: {worker_stats['completed_jobs']}")
        print(f"   Jobs failed: {worker_stats['failed_jobs']}")
        print(f"   Success rate: {worker_stats['success_rate']:.1%}")
        
        print(f"\n🎯 Overall System Resilience:")
        print(f"   ✅ Successful tasks: {succeeded}")
        print(f"   ❌ Failed tasks: {failed}")
        print(f"   📬 Queue handled: {queue_stats['total_processed']} messages reliably")
        print(f"   🛡️  System remained operational throughout!")
        
        # Cleanup
        resilient_worker.stop()
        resilient_queue.stop()
        
        print(f"\n⏱️  Total processing time: {total_time:.1f} seconds")
        
        self.print_info("""
🛡️  Service vs Queue + Worker Resilience Comparison:
   • Service building block: One failure can freeze entire system
   • Queue + Worker building blocks: Fault isolation and message persistence
   • Queue provided message persistence (no lost tasks)
   • Failed Worker tasks didn't crash the Queue or other Workers
   • Other tasks continued processing normally  
   • Queue subscriber handled errors gracefully
   • System maintained responsiveness throughout failures
   • Each failure was isolated and logged
   
This is why system thinkers choose Queue + Worker over Service for critical systems!
""")
        
        # Multiple choice reflections for Experiment 4
        self.print_header("EXPERIMENT 4 REFLECTIONS", style="sub")
        
        # Question 1
        self.ask_multiple_choice(
            "How did the Queue + Worker system handle individual task failures differently than a blocking Service?",
            [
                "It prevented all failures from happening",
                "It isolated failures so they didn't crash the entire system",
                "It automatically retried failed tasks until they succeeded"
            ],
            [
                "Not quite! The Queue + Worker system doesn't prevent failures - some tasks still failed as designed. The key is how gracefully it handled those failures without affecting other parts of the system.",
                "Excellent understanding! This is fault isolation in action. When a Worker task failed, it didn't crash the Queue, other Workers, or the user interface. Each failure was contained, logged, and the system kept running normally.",
                "Great thinking about retry mechanisms! While Queue + Worker systems can include retry logic, that wasn't the main lesson here. The key insight is that failures were isolated and didn't cascade to affect other components."
            ]
        )
        
        # Question 2
        self.ask_multiple_choice(
            "What role did the Queue building block play in system resilience?",
            [
                "It stored messages reliably even when Workers failed",
                "It made Workers process tasks faster to avoid failures",
                "It detected and prevented potential failures before they happened"
            ],
            [
                "Perfect! The Queue building block provided message persistence and durability. Even when Workers failed, the messages were safely stored and could be processed later. This reliability is crucial for business-critical operations.",
                "Not exactly! The Queue doesn't make Workers faster or change their failure rate. Its value is in providing reliable message storage and routing, ensuring no work is lost even when failures occur.",
                "The Queue doesn't predict or prevent failures. Its strength is in graceful failure handling - ensuring messages aren't lost and the system remains operational even when individual components fail."
            ]
        )
        
        # Question 3
        self.ask_multiple_choice(
            "Why is this fault isolation crucial for business systems like payment processing?",
            [
                "Because payment systems need to process transactions faster",
                "Because one failed payment shouldn't crash the entire payment system",
                "Because payment systems need better user interfaces"
            ],
            [
                "Speed is important for payments, but not the primary concern here. The critical issue is reliability - ensuring that payment processing continues even when individual transactions fail or external services have problems.",
                "Absolutely critical insight! In payment systems, individual transaction failures are inevitable (expired cards, insufficient funds, network timeouts). The system must handle these gracefully without affecting other customers' transactions or crashing the entire platform.",
                "User experience matters, but the fundamental issue is system reliability. Even with a perfect UI, if payment failures crash the system, no customers can complete purchases. Fault isolation ensures business continuity."
            ]
        )
        
        # This is the final experiment, so run conclusion
        self.run_conclusion()
    
    
    def run_conclusion(self):
        """Lab conclusion and next steps"""
        self.print_header("CONGRATULATIONS! LAB COMPLETED")
        
        print(f"\n🎉 Well done, {self.student_name}!\n")
        
        self.typewriter_print("You've discovered firsthand why system thinkers choose Queue + Worker over Service building blocks:")
        
        print(f"""
🔍 Your Service vs Queue + Worker Discoveries:
   • Service building block: Blocking operations create terrible user experiences
   • Queue building block: Enables message persistence, routing, and load balancing
   • Worker building block: Provides non-blocking background processing power
   • Service alone: Sequential, blocking, single point of failure
   • Queue + Worker together: Responsive, scalable, resilient systems
   • Queue distribution enables horizontal scaling across multiple Workers
   • Queue + Worker fault isolation prevents system-wide failures

💡 THE SYSTEM THINKING INSIGHT - Same Work, Different Building Blocks:
   • You executed the SAME work functions (process_image_work, send_email_work, etc.)
   • Service building block: Executed work synchronously, blocking the UI
   • Worker building block: Executed work asynchronously, never blocking the UI
   • The BUSINESS LOGIC was identical - only the EXECUTION PATTERN changed!
   • This separation is the essence of system thinking: separate WHAT from HOW
   • Building blocks don't change the work - they change how and when it executes
   • Good architects choose building blocks based on execution requirements, not work type

📊 Your Building Block Comparison Times:
   • Service Building Block: {self.experiment_times.get('experiment_1', 0):.1f}s (UI frozen entire time)
   • Queue + Worker: {self.experiment_times.get('experiment_2', 0):.1f}s (UI always responsive)
   • Queue → Multiple Workers: {self.experiment_times.get('experiment_3', 0):.1f}s (distributed processing)
   • Queue + Worker Resilience: {self.experiment_times.get('experiment_4', 0):.1f}s (handled failures gracefully)

🏗️ You now understand why these companies use Queue + Worker instead of Service alone:
   • Instagram: Queue routes photo jobs to Worker farms (not blocking Service calls)
   • Netflix: Queue distributes video encoding to Worker clusters (not sequential Service processing)
   • Gmail: Queue handles email delivery through Worker processes (not blocking Service requests)
   • Uber: Queue manages ride requests across Worker services (not single Service bottleneck)

🎓 You've completed your system thinking transformation! You now think like an AI-empowered system thinker who understands:
   • When to use Service building blocks (fast, synchronous operations)
   • When to use Queue + Worker building blocks (scalable, resilient, async operations)
   • How building block choices impact user experience and system reliability

Master the 7 building blocks + 3 external entities for AI-era system thinking!
""")
        
        print("\n" + "🎯" * 40)
        self.typewriter_print("🎯 Thank you for completing the discovery lab! 🎯", speed=0.05)
        print("🎯" * 40 + "\n")
    
    def run(self, experiment_num: Optional[int] = None):
        """Run the complete lab experience or a specific experiment
        
        Args:
            experiment_num: Optional experiment number (1-4) to run directly
        """
        try:
            if experiment_num is not None:
                # Run specific experiment directly
                print(f"\n🎯 Running Experiment {experiment_num} directly...\n")
                self.student_name = "Test User"  # Default name for direct runs
                
                if experiment_num == 1:
                    self.experiment_1_blocking()
                elif experiment_num == 2:
                    self.experiment_2_async()
                elif experiment_num == 3:
                    self.experiment_3_parallel()
                elif experiment_num == 4:
                    self.experiment_4_resilience()
                else:
                    print(f"❌ Invalid experiment number: {experiment_num}")
                    print("   Valid experiments are 1-4")
                    return
                
                # Show summary after single experiment
                print("\n" + "="*80)
                print("🔬 EXPERIMENT COMPLETE")
                print("="*80)
                if experiment_num in [1, 2, 3, 4]:
                    exp_time = self.experiment_times.get(f'experiment_{experiment_num}', 0)
                    print(f"⏱️  Experiment {experiment_num} time: {exp_time:.1f}s")
            else:
                # Run full lab experience
                self.run_welcome()
                self.experiment_1_blocking()
                # The experiments chain themselves based on user input
                # Conclusion is called from experiment_4_resilience if user completes all
        except KeyboardInterrupt:
            print("\n\n⚠️  Lab interrupted by user.")
            print("Thank you for participating in the discovery lab.")
        except Exception as e:
            print(f"\n\n❌ An error occurred: {e}")
            print("Please try running the lab again.")


def main():
    """Main entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Systems Thinking in the AI Era I - Lesson 5 Discovery Lab",
        epilog="Run without arguments for full lab experience, or specify experiment number for direct access."
    )
    parser.add_argument(
        "experiment",
        nargs="?",
        type=int,
        choices=[1, 2, 3, 4],
        help="Optional: Run specific experiment directly (1-4)"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Disable typewriter effect for faster output"
    )
    
    args = parser.parse_args()
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║     BUILDING BLOCK MASTERY - INTERACTIVE LAB EXPERIENCE             ║
║     Lesson 5: Queue + Worker Async Processing Discovery             ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Create and configure lab
    lab = LabExperience()
    
    # Set fast mode if requested
    if args.fast:
        lab.instant_print = True
        print("⚡ Fast mode enabled - typewriter effect disabled\n")
    
    # Run the lab
    lab.run(args.experiment)


if __name__ == "__main__":
    main()