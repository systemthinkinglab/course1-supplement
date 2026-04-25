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
Lesson 8: Time + Worker - Scheduled Processing Discovery Lab
Interactive lab exploring automated Time + Worker patterns and background processing

This lab demonstrates system thinking skills that complement AI capabilities:
1. Manual vs automated Worker task execution
2. Time + Worker pattern for automated processing
3. Multiple Time entities for different business domains
4. Error handling and system resilience

Usage:
  python3 lesson8_interactive_lab.py           # Run complete lab
  python3 lesson8_interactive_lab.py 1         # Run experiment 1 only
  python3 lesson8_interactive_lab.py 2         # Run experiment 2 only
  python3 lesson8_interactive_lab.py 3         # Run experiment 3 only
  python3 lesson8_interactive_lab.py 4         # Run experiment 4 only
  python3 lesson8_interactive_lab.py --help    # Show all options
"""

import time
import random
import sys
import os
import threading
import argparse
from datetime import datetime
from typing import Optional, Dict, List

# Add the repository root to the Python path for imports
# This allows running from: python labs/course1/lab2_time_worker.py
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, repo_root)

try:
    from building_blocks.building_blocks import Worker
    from building_blocks.external_entities import Time
except ImportError:
    print("Error: Could not import building_blocks module.")
    print("Please run this script from the repository root:")
    print("  cd system-thinking-in-the-ai-era")
    print("  python labs/course1/lab2_time_worker.py")
    sys.exit(1)


class TimeWorkerLabExperience:
    def __init__(self, instant_print=False):
        self.student_name = ""
        self.experiment_times = {}
        self.typewriter_speed = 0.03
        self.instant_print = instant_print
        self.print_lock = threading.Lock()  # Thread-safe printing

    def typewriter_print(self, text: str, speed: Optional[float] = None, end: str = "\n"):
        """Print text with typewriter effect (thread-safe)"""
        with self.print_lock:
            if self.instant_print:
                print(text, end=end)
                return
            if speed is None:
                speed = self.typewriter_speed
            for char in text:
                print(char, end='', flush=True)
                if char not in [' ', '\n', '\t']:
                    time.sleep(speed)
            print(end=end)
    
    def direct_print(self, text: str, end: str = "\n"):
        """Print text directly without typewriter effect (thread-safe)"""
        with self.print_lock:
            print(text, end=end)

    def ask_multiple_choice(self, question: str, choices: List[str], responses: List[str]) -> str:
        """Ask a multiple choice question with educational responses"""
        print()
        self.typewriter_print("🤔 " + question)
        print()
        
        for i, choice in enumerate(choices, 1):
            print(f"   {i}. {choice}")
        
        while True:
            user_input = input("\n👤 Your choice (1, 2, or 3): ").strip()
            if user_input in ['1', '2', '3']:
                choice_index = int(user_input) - 1
                print()
                self.typewriter_print("✨ " + responses[choice_index])
                return user_input
            else:
                print("Please enter 1, 2, or 3.")

    def welcome(self):
        """Welcome message and student name input"""
        print("="*70)
        self.typewriter_print("🎯 TIME + WORKER DISCOVERY LAB - AUTOMATED PROCESSING PATTERNS")
        print("="*70)
        print()
        self.typewriter_print("Welcome to an interactive exploration of automated Time + Worker patterns!")
        self.typewriter_print("You'll experience the power of Time + Worker combinations through hands-on experiments.")
        print()
        
        self.student_name = input("👤 Please enter your name: ").strip()
        if not self.student_name:
            self.student_name = "Student"
        
        print()
        self.typewriter_print(f"Hello {self.student_name}! Let's discover how Time + Worker patterns transform business operations.")
        print()

    def experiment_1_manual_execution(self):
        """Experiment 1: Manual Worker Task Execution - Experience the pain"""
        print("\n" + "="*60)
        self.typewriter_print("📋 EXPERIMENT 1: MANUAL WORKER TASK EXECUTION")
        print("="*60)
        
        self.typewriter_print("You'll experience what it's like to manually execute business Worker tasks.")
        self.typewriter_print("🔧 Notice: You're essentially acting as a human Time entity for Worker building blocks!")
        self.typewriter_print("⚠️  IMPORTANT: You must type each command EXACTLY as shown!")
        self.typewriter_print("Any typo means starting over - just like in production systems.")
        print()
        
        # Define the tedious commands
        commands = {
            "Daily Reports": "python /opt/business/reports/generate_sales_report.py --date=$(date +%Y-%m-%d) --output=/var/reports/daily/ --format=pdf --include-metrics=revenue,transactions,customers --email-to=management@company.com",
            "User Notifications": "bash /scripts/notifications/send_customer_updates.sh --segment=active --template=daily_digest --personalized=true --batch-size=1000 --retry-failures=3",
            "Data Cleanup": "sudo find /var/log -name '*.log' -mtime +30 -exec rm {} \\; && df -h | grep -E '^/dev/' | awk '{print $5}' | sed 's/%//'"
        }
        
        start_time = time.time()
        mistakes = 0
        task_times = []
        
        for task_name, command in commands.items():
            task_start = time.time()
            
            self.typewriter_print(f"\n🚨 WORKER TASK: {task_name}")
            self.typewriter_print("📋 Type this command EXACTLY (copy-paste is disabled in production!):")
            print(f"\n   {command}\n")
            
            attempts = 0
            while True:
                attempts += 1
                user_input = input("👤 Type command: ").strip()
                
                if user_input == command:
                    self.typewriter_print("✅ Command accepted! Executing Worker task...")
                    
                    # Simulate Worker task execution with progress
                    if task_name == "Daily Reports":
                        self.typewriter_print(f"🔧 [Worker Building Block Starting] Generating daily reports at {datetime.now().strftime('%H:%M:%S')}")
                        for i in range(3):
                            time.sleep(1)
                            self.typewriter_print(f"   ... processing data ({i+1}/3)")
                        self.typewriter_print("✅ [Worker Building Block Complete] Daily reports generated")
                    
                    elif task_name == "User Notifications":
                        self.typewriter_print(f"🔧 [Worker Building Block Starting] Sending notifications at {datetime.now().strftime('%H:%M:%S')}")
                        for i in range(2):
                            time.sleep(1)
                            self.typewriter_print(f"   ... sending batch ({i+1}/2)")
                        self.typewriter_print("✅ [Worker Building Block Complete] Notifications sent")
                    
                    else:  # Data Cleanup
                        self.typewriter_print(f"🔧 [Worker Building Block Starting] Cleaning data at {datetime.now().strftime('%H:%M:%S')}")
                        for i in range(4):
                            time.sleep(1)
                            self.typewriter_print(f"   ... removing old files ({i+1}/4)")
                        self.typewriter_print("✅ [Worker Building Block Complete] Cleanup finished")
                    
                    break
                else:
                    mistakes += 1
                    self.typewriter_print("❌ INCORRECT! Every character must match exactly.")
                    
                    # Show hints about what went wrong
                    if len(user_input) < len(command):
                        self.typewriter_print("💡 Your command is too short")
                    elif len(user_input) > len(command):
                        self.typewriter_print("💡 Your command is too long")
                    else:
                        # Find first difference
                        for i, (c1, c2) in enumerate(zip(command, user_input)):
                            if c1 != c2:
                                self.typewriter_print(f"💡 First error at position {i+1}: expected '{c1}', got '{c2}'")
                                break
                    
                    if attempts >= 2:
                        self.typewriter_print("😤 This is exhausting! And it's only 9 AM...")
                    if attempts >= 3:
                        self.typewriter_print("🔥 In production, these mistakes could break the system!")
                    print()
            
            task_time = time.time() - task_start
            task_times.append(task_time)
            
            # Simulate forgetting or delays between tasks
            if task_name == "Daily Reports":
                self.typewriter_print("\n😴 You got pulled into a meeting...")
                time.sleep(2)
                self.typewriter_print("⏰ Oh no! Almost forgot about notifications!")
            elif task_name == "User Notifications":
                self.typewriter_print("\n☕ Quick coffee break...")
                time.sleep(2)
                self.typewriter_print("🚨 ALERT: Disk space at 95%! Need cleanup NOW!")
        
        total_time = time.time() - start_time
        
        self.typewriter_print(f"\n📊 MANUAL EXECUTION SUMMARY:")
        self.typewriter_print(f"   Total time: {total_time:.1f} seconds")
        self.typewriter_print(f"   Worker building blocks manually triggered: 3")
        self.typewriter_print(f"   Typing mistakes: {mistakes}")
        self.typewriter_print(f"   Average time per Worker task: {sum(task_times)/len(task_times):.1f} seconds")
        self.typewriter_print(f"   😰 Stress level: EXTREME")
        self.typewriter_print(f"   🧠 Mental load: Can't focus on anything else")
        self.typewriter_print(f"   🔧 Key insight: You were the Time entity manually triggering Worker building blocks!")
        self.typewriter_print(f"   💀 Reality: This is just 3 Worker tasks. Real ops teams manage 50+")
        
        # Multiple choice reflections
        self.ask_multiple_choice(
            "What was the most frustrating aspect of manual command execution?",
            [
                "The commands weren't that difficult to type",
                "The complexity and length of commands with high error risk",
                "I could memorize these commands with practice"
            ],
            [
                "That's understandable - they might seem manageable at first glance. However, you made {} mistakes in this calm demo. Complex commands under production pressure create much higher error rates. This is why experienced system thinkers prefer automation for reliability.".format(mistakes),
                "Exactly! Complex commands create cognitive overload and high error risk. You made {} mistakes in a calm demo - imagine during an outage! This is why system thinkers automate everything. Manual command execution is organizational debt that AI cannot solve.".format(mistakes),
                "That's a natural thought - we often feel we can memorize patterns. However, commands change, parameters evolve, and even with {} mistakes here, memory fails under stress. Experienced system thinkers know that reliable operations need automation, not human memory.".format(mistakes)
            ]
        )
        
        self.ask_multiple_choice(
            "If you had to scale this to run every hour for a business with 1000+ users, what would be the biggest challenge?",
            [
                "The servers would get overloaded",
                "The database would run out of space",
                "The system would break down due to human limitations"
            ],
            [
                "That's a valid concern about infrastructure. Servers can be scaled horizontally though. The fundamental challenge is that manual processes require human operators who can't work continuously, make mistakes, and forget tasks. Technical scaling is actually easier than human scaling.",
                "Storage is definitely important to monitor. However, the core limitation here is human capacity - people can't manually trigger Worker tasks 24/7 without breaks, vacation, or mistakes. This is why automated Time + Worker patterns become essential for business reliability.",
                "Absolutely correct! Manual processes don't scale because humans can't work 24/7 with perfect reliability. This is exactly why Instagram, Netflix, and every major platform use Time + Worker patterns for their critical business operations."
            ]
        )
        
        self.ask_multiple_choice(
            "How does this manual experience relate to real-world business systems?", 
            [
                "Manual processes are fine for small businesses",
                "Most business Worker tasks need automated Time entities to be reliable",
                "This was just a simplified demo"
            ],
            [
                "That's a common initial thought for smaller operations. However, even small businesses benefit greatly from automated billing, backups, and notifications. Manual processes create reliability challenges at any size, and Time + Worker patterns help from day one.",
                "Brilliant connection! Every successful business relies on automated Time + Worker patterns - from Netflix billing cycles to Instagram content moderation. System thinkers understand that reliable business operations require Time + Worker patterns, not manual intervention.",
                "It might seem simplified, but this demo demonstrates exactly the same challenges that real businesses face! The frustration you felt manually triggering Worker tasks is the same problem that led to automated Time + Worker patterns in every major platform."
            ]
        )
        
        self.ask_multiple_choice(
            "What building block pattern did you just experience manually?",
            [
                "I was implementing a Service building block",
                "I was managing a Queue of tasks",
                "I was acting as the Time entity triggering Worker tasks"
            ],
            [
                "I can see the connection - there was interaction happening. However, Services handle synchronous request/response patterns. You were actually triggering background tasks that run independently, which is the Worker building block pattern. Services block and wait, but these tasks ran in the background.",
                "Great observation about the multiple Worker tasks! While there were several tasks, you weren't managing a Queue. You were actually the Time entity triggering Worker building blocks directly. A Queue would store these tasks for processing, but you were manually initiating each one.",
                "Brilliant connection! You were literally the human Time entity, manually triggering Worker tasks. The commands you typed kicked off background jobs (reports, notifications, cleanup) - classic Worker building block tasks. Automation replaces YOU with a reliable Time entity."
            ]
        )
        
        self.experiment_times["experiment_1"] = total_time
        
        # Pause before next experiment
        print("\n" + "="*50)
        self.typewriter_print("🎓 EXPERIMENT 1 COMPLETE!")
        self.typewriter_print("You've experienced the pain and limitations of manual Worker task execution.")
        self.typewriter_print(f"You made {mistakes} typing mistakes - imagine the stress in production!")
        self.typewriter_print("Next: Discover how Time + Worker automation transforms this experience.")
        print()
        input("👤 Press Enter when you're ready for Experiment 2...")
        
        return total_time

    def experiment_2_basic_automation(self):
        """Experiment 2: Basic Time + Worker Automation - Feel the relief"""
        print("\n" + "="*60)
        self.typewriter_print("⚡ EXPERIMENT 2: TIME + WORKER AUTOMATION")
        print("="*60)
        
        self.typewriter_print("Now you'll experience the same Worker tasks with automated Time + Worker patterns!")
        self.typewriter_print("Notice how your role changes from manual operator to system observer.")
        print()
        
        start_time = time.time()
        
        # Create Time entity for triggering Worker tasks
        business_time_entity = Time("business_scheduler")
        
        # Create Worker building block for background processing
        task_worker = Worker("task_processor")
        
        # Business Worker tasks (same functionality, but now automated)
        def process_daily_reports(data=None):
            processing_time = random.uniform(3, 5)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"📊 Daily reports completed automatically at {datetime.now().strftime('%H:%M:%S')}")
            return {"status": "completed", "processing_time": processing_time}

        def process_user_notifications(data=None):
            processing_time = random.uniform(2, 4)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"📧 User notifications sent automatically at {datetime.now().strftime('%H:%M:%S')}")
            return {"status": "completed", "processing_time": processing_time}

        def cleanup_old_data(data=None):
            processing_time = random.uniform(4, 6)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"🧹 Data cleanup completed automatically at {datetime.now().strftime('%H:%M:%S')}")
            return {"status": "completed", "processing_time": processing_time}
        
        # Register Worker task types with the Worker building block
        task_worker.register_job_type("daily_reports", process_daily_reports)
        task_worker.register_job_type("user_notifications", process_user_notifications)
        task_worker.register_job_type("data_cleanup", cleanup_old_data)
        
        # Set up Time entity triggers for Worker tasks (shorter intervals for demo)
        @business_time_entity.recurring_trigger(interval_seconds=8, start_delay=2)
        def trigger_daily_reports():
            self.direct_print("⏰ Time trigger: Scheduling daily reports")
            job_id = task_worker.submit_job("daily_reports", {})
            self.direct_print(f"📝 Job {job_id} submitted for background processing")
        
        @business_time_entity.recurring_trigger(interval_seconds=12, start_delay=5)
        def trigger_user_notifications():
            self.direct_print("⏰ Time trigger: Scheduling user notifications")
            job_id = task_worker.submit_job("user_notifications", {})
            self.direct_print(f"📝 Job {job_id} submitted for background processing")
        
        @business_time_entity.recurring_trigger(interval_seconds=15, start_delay=8)
        def trigger_data_cleanup():
            self.direct_print("⏰ Time trigger: Scheduling data cleanup")
            job_id = task_worker.submit_job("data_cleanup", {})
            self.direct_print(f"📝 Job {job_id} submitted for background processing")
        
        # Start the automated Time + Worker system
        self.typewriter_print("🚀 Starting automated Time + Worker processing...")
        self.typewriter_print("👀 Watch how Worker tasks are triggered automatically by Time entity!")
        self.typewriter_print("⚡ Notice: Worker tasks run in background without blocking the system")
        self.typewriter_print("🔄 Observe for 25 seconds...\n")
        
        business_time_entity.start_time_monitoring()
        task_worker.start()
        
        try:
            start_time = time.time()
            while time.time() - start_time < 25:  # Run for 25 seconds
                elapsed = int(time.time() - start_time)
                stats = task_worker.get_stats()
                
                self.direct_print(f"\n🔄 Automated system running... ({elapsed}s elapsed)")
                self.direct_print(f"📈 Worker stats: Completed: {stats['completed_jobs']}, "
                                f"Failed: {stats['failed_jobs']}, "
                                f"Success Rate: {stats['success_rate']:.1f}%")
                self.direct_print("✅ You can focus on other work while automation handles tasks!")
                time.sleep(5)
        
        except KeyboardInterrupt:
            self.typewriter_print("\n🛑 Stopping automated Time + Worker system...")
        
        finally:
            business_time_entity.stop_time_monitoring()
            task_worker.stop()
            
            # Show final statistics
            total_time = time.time() - start_time
            final_stats = task_worker.get_stats()
            self.typewriter_print(f"\n📊 AUTOMATION SUMMARY:")
            self.typewriter_print(f"   Total elapsed time: {total_time:.1f} seconds")
            self.typewriter_print(f"   Jobs completed: {final_stats['completed_jobs']}")
            self.typewriter_print(f"   Jobs failed: {final_stats['failed_jobs']}")
            self.typewriter_print(f"   Total jobs processed: {final_stats['total_jobs']}")
            self.typewriter_print(f"   Success rate: {final_stats['success_rate']:.1f}%")
            self.typewriter_print(f"   🎯 System ran automatically without human intervention!")
            self.typewriter_print(f"   ⚡ You were free to focus on other work for {total_time:.1f} seconds!")
        
        # Multiple choice reflections
        self.ask_multiple_choice(
            "How did the automated approach feel different from manual execution?",
            [
                "The tasks ran faster than before",
                "The output was more colorful and detailed", 
                "Much more relaxing - I could focus on other things"
            ],
            [
                "I understand why it might seem faster! The Worker task processing speed was actually similar though. The key difference is that automation eliminates the need for constant human attention and intervention, allowing you to be productive while Worker tasks run in the background.",
                "The visual presentation was enhanced, but that wasn't the main transformation. The key aspect is how automation frees you from manual Worker task triggering, letting you focus on strategic work while the Time + Worker system handles routine operations automatically.",
                "Perfect observation! This is exactly how Time + Worker patterns transform work. Instead of being stuck manually triggering Worker tasks, you become a strategic observer. This is the difference between code writer and AI-empowered system thinker approaches to system design."
            ]
        )
        
        self.ask_multiple_choice(
            "What role did the Worker building block play in this automation?",
            [
                "It made the tasks run much faster",
                "It handled background processing without blocking the system",
                "It provided better logging and output formatting"
            ],
            [
                "That's a natural observation! While efficiency can improve, speed wasn't the main benefit. Worker building blocks enable background processing so Worker tasks don't block the main system. The key advantage is that you can continue other work while Worker tasks process asynchronously in the background.",
                "Exactly right! Worker building blocks are essential for non-blocking background processing. This is how Gmail sends millions of emails, how Uber processes payments, and how every major platform handles heavy work without freezing user interfaces.",
                "The presentation was cleaner, but that wasn't the primary function. Worker building blocks provide background processing capability, allowing Worker tasks to run without blocking the main system thread. This enables responsive systems that can handle multiple operations simultaneously."
            ]
        )
        
        self.ask_multiple_choice(
            "How does this automation pattern apply to real business systems?",
            [
                "It's only useful for tech companies",
                "Manual processes are more flexible than automation",
                "Every business needs automated Time + Worker patterns for reliability"
            ],
            [
                "I can see why it might seem tech-focused! However, restaurants use automated ordering systems, retail stores use automated inventory management, and service businesses use automated billing. Time + Worker patterns are actually universal business enablers across all industries.",
                "That's an interesting perspective on flexibility! While manual processes might seem adaptable, automation actually provides much more flexibility - you can easily adjust Time triggers, add new Worker task types, and scale processing power. Manual processes can lock you into human limitations and availability constraints.",
                "Absolutely correct! From banking transactions to email marketing to inventory updates, every successful business relies on automated Time + Worker patterns. System thinkers understand that business growth requires Time + Worker patterns for operational reliability."
            ]
        )
        
        # Pause before next experiment
        print("\n" + "="*50)
        self.typewriter_print("🎓 EXPERIMENT 2 COMPLETE!")
        self.typewriter_print("You've experienced the relief and power of automated Time + Worker patterns!")
        self.typewriter_print("Next: Explore advanced patterns with multiple Time entities for different business domains.")
        print()
        input("👤 Press Enter when you're ready for Experiment 3...")
        
        return final_stats['completed_jobs']

    def experiment_3_advanced_scheduling(self):
        """Experiment 3: Advanced Time + Worker Patterns - Multiple Time entities sharing Worker tasks"""
        print("\n" + "="*60)
        self.typewriter_print("🏢 EXPERIMENT 3: ADVANCED TIME + WORKER PATTERNS")
        print("="*60)
        
        self.typewriter_print("Now you'll discover why multiple Time entities are essential when different business")
        self.typewriter_print("domains need the SAME Worker building blocks executed at DIFFERENT frequencies!")
        self.typewriter_print("This shows the beauty of separation of concerns in system design.")
        print()
        
        # Preview the scenario
        self.typewriter_print("🎭 THE SCENARIO:")
        self.typewriter_print("You run an e-commerce platform with two critical domains:")
        print()
        self.typewriter_print("📈 CUSTOMER ANALYTICS DOMAIN:")
        self.typewriter_print("   • Needs real-time insights for live dashboards")
        self.typewriter_print("   • Business analysts refreshing reports constantly")
        self.typewriter_print("   • Requires frequent data processing")
        print()
        self.typewriter_print("🔧 COMPLIANCE & AUDIT DOMAIN:")
        self.typewriter_print("   • Needs the same data for regulatory reports")
        self.typewriter_print("   • Legal requirements for periodic compliance checks")
        self.typewriter_print("   • Different timing requirements")
        print()
        self.typewriter_print("💡 KEY INSIGHT: Both domains need the SAME Worker tasks, but triggered by different Time entities!")
        self.typewriter_print("Imagine trying to create one Time entity that handles both requirements...")
        print()
        
        # Create specialized Time entities for different business domains
        analytics_time_entity = Time("customer_analytics")
        compliance_time_entity = Time("compliance_audit")
        
        # Single Worker building block shared by both domains (same functionality, different timing)
        shared_worker = Worker("e_commerce_processor")
        
        # Shared Worker tasks that both domains need (same functionality, different frequencies)
        def process_sales_data(data=None):
            domain = data.get('domain', 'unknown') if data else 'unknown'
            processing_time = random.uniform(1.5, 2.5)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"📊 Sales data processed for {domain} at {datetime.now().strftime('%H:%M:%S')}")
            return {"worker_task": "sales_data", "domain": domain, "processing_time": processing_time}
        
        def generate_user_behavior_report(data=None):
            domain = data.get('domain', 'unknown') if data else 'unknown'
            processing_time = random.uniform(2, 3)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"👥 User behavior report generated for {domain} at {datetime.now().strftime('%H:%M:%S')}")
            return {"worker_task": "user_behavior", "domain": domain, "processing_time": processing_time}
        
        def audit_transaction_logs(data=None):
            domain = data.get('domain', 'unknown') if data else 'unknown'
            processing_time = random.uniform(1, 2)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"🔍 Transaction logs audited for {domain} at {datetime.now().strftime('%H:%M:%S')}")
            return {"worker_task": "transaction_audit", "domain": domain, "processing_time": processing_time}
        
        # Register shared Worker tasks with the single Worker building block
        shared_worker.register_job_type("sales_data", process_sales_data)
        shared_worker.register_job_type("user_behavior", generate_user_behavior_report)
        shared_worker.register_job_type("transaction_audit", audit_transaction_logs)
        
        # ANALYTICS DOMAIN: Needs frequent updates (high-frequency Time triggers)
        @analytics_time_entity.recurring_trigger(interval_seconds=4, start_delay=1)
        def analytics_sales_data():
            self.direct_print("📈 [ANALYTICS] Frequent trigger: Processing sales data for dashboards")
            shared_worker.submit_job("sales_data", {"domain": "ANALYTICS"})
        
        @analytics_time_entity.recurring_trigger(interval_seconds=6, start_delay=2)
        def analytics_user_behavior():
            self.direct_print("📈 [ANALYTICS] Frequent trigger: User behavior for live insights")
            shared_worker.submit_job("user_behavior", {"domain": "ANALYTICS"})
        
        @analytics_time_entity.recurring_trigger(interval_seconds=8, start_delay=3)
        def analytics_transaction_audit():
            self.direct_print("📈 [ANALYTICS] Frequent trigger: Transaction patterns analysis")
            shared_worker.submit_job("transaction_audit", {"domain": "ANALYTICS"})
        
        # COMPLIANCE DOMAIN: Needs less frequent but regular updates (lower-frequency Time triggers)
        @compliance_time_entity.recurring_trigger(interval_seconds=12, start_delay=5)
        def compliance_sales_data():
            self.direct_print("🏛️  [COMPLIANCE] Regulatory trigger: Sales data for compliance reports")
            shared_worker.submit_job("sales_data", {"domain": "COMPLIANCE"})
        
        @compliance_time_entity.recurring_trigger(interval_seconds=18, start_delay=8)
        def compliance_user_behavior():
            self.direct_print("🏛️  [COMPLIANCE] Regulatory trigger: User behavior for audit trail")
            shared_worker.submit_job("user_behavior", {"domain": "COMPLIANCE"})
        
        @compliance_time_entity.recurring_trigger(interval_seconds=15, start_delay=10)
        def compliance_transaction_audit():
            self.direct_print("🏛️  [COMPLIANCE] Regulatory trigger: Full transaction audit")
            shared_worker.submit_job("transaction_audit", {"domain": "COMPLIANCE"})
        
        self.typewriter_print("📈 Starting Analytics Time entity (high-frequency for live dashboards)...")
        self.typewriter_print("🏛️  Starting Compliance Time entity (lower-frequency for regulatory needs)...")
        self.typewriter_print("🔧 Notice: ONE Worker building block handling the same tasks, but TWO different Time patterns!")
        self.typewriter_print("💡 Key insight: Worker tasks do their job well, Time entities decide timing for their domain")
        self.typewriter_print("🔄 Observing domain-separated Time + Worker patterns for 22 seconds...\n")
        
        # Start all systems
        analytics_time_entity.start_time_monitoring()
        compliance_time_entity.start_time_monitoring()
        shared_worker.start()
        
        analytics_jobs = 0
        compliance_jobs = 0
        
        try:
            start_time = time.time()
            while time.time() - start_time < 22:  # Run for 22 seconds
                elapsed = int(time.time() - start_time)
                
                # Count jobs by domain
                completed_jobs = shared_worker.completed_jobs
                analytics_jobs = sum(1 for job in completed_jobs if job.get('result', {}).get('domain') == 'ANALYTICS')
                compliance_jobs = sum(1 for job in completed_jobs if job.get('result', {}).get('domain') == 'COMPLIANCE')
                
                self.direct_print(f"\n🏢 Domain-separated Time + Worker patterns running... ({elapsed}s elapsed)")
                self.direct_print(f"   📈 Analytics jobs (high-freq): {analytics_jobs} completed")
                self.direct_print(f"   🏛️  Compliance jobs (low-freq): {compliance_jobs} completed")
                self.direct_print("   💡 Same Worker tasks, different Time entity requirements!")
                
                time.sleep(4)
                
        except KeyboardInterrupt:
            self.typewriter_print("\n🛑 Stopping all Time entities...")
        
        finally:
            analytics_time_entity.stop_time_monitoring()
            compliance_time_entity.stop_time_monitoring()
            shared_worker.stop()
            
            # Final count
            completed_jobs = shared_worker.completed_jobs
            analytics_final = sum(1 for job in completed_jobs if job.get('result', {}).get('domain') == 'ANALYTICS')
            compliance_final = sum(1 for job in completed_jobs if job.get('result', {}).get('domain') == 'COMPLIANCE')
            
            self.typewriter_print(f"\n📊 DOMAIN SEPARATION SUMMARY:")
            self.typewriter_print(f"   📈 Analytics domain: {analytics_final} jobs (high-frequency)")
            self.typewriter_print(f"   🏛️  Compliance domain: {compliance_final} jobs (lower-frequency)")
            self.typewriter_print(f"   🔧 Total shared Worker tasks executed: {analytics_final + compliance_final}")
            self.typewriter_print(f"   💡 Same Worker building block, different Time entity timing - perfect separation!")
            self.typewriter_print(f"   🎯 Each domain got exactly the frequency it needed!")
        
        # Multiple choice reflections
        self.ask_multiple_choice(
            "What would happen if you tried to use ONE Time entity for both Analytics and Compliance needs?",
            [
                "It would be simpler and more efficient",
                "You'd have to compromise - either too frequent for Compliance or too slow for Analytics",
                "One Time entity would use less memory"
            ],
            [
                "That's a natural thought about simplicity! However, one Time entity would create a complex mess of conditional logic trying to handle different timing requirements. You'd end up with analytics getting stale data or compliance systems being overwhelmed with unnecessary processing.",
                "Exactly right! This is the core problem that multiple Time entities solve. Analytics needs real-time updates while Compliance needs periodic reports. One Time entity forces you to pick a frequency that doesn't serve either domain well - classic architectural compromise trap.",
                "Resource efficiency is worth considering! However, the memory savings would be tiny compared to the business impact. Forcing different business domains into one timing pattern creates operational problems far more expensive than running separate Time entities."
            ]
        )
        
        self.ask_multiple_choice(
            "What's the key architectural insight from seeing the same Worker tasks triggered differently?",
            [
                "Worker building blocks should focus on their core functionality, Time entities handle timing requirements",
                "It's better to write different Worker tasks for different domains",
                "Multiple Time entities create unnecessary complexity"
            ],
            [
                "Perfect separation of concerns understanding! This is exactly how system thinkers approach architecture - Worker building blocks encapsulate 'how to do the work' while Time entities handle 'when to do the work.' This separation makes systems maintainable and allows business domains to evolve independently - interface design that AI cannot replicate.",
                "That might seem logical at first! However, duplicating Worker building block code for different domains creates maintenance nightmares and violates the DRY principle. The beauty is that the same business logic (processing sales data) can serve multiple domains with different timing requirements.",
                "I understand the complexity concern! However, multiple Time entities actually reduce complexity by separating business domain concerns. Trying to handle all timing requirements in one place creates more complex conditional logic and harder-to-understand code."
            ]
        )
        
        self.ask_multiple_choice(
            "How does this pattern apply to your future system designs?",
            [
                "Always create separate Time entities for different teams or departments",
                "Keep all timing logic in one Time entity for consistency",
                "Identify when different business domains need the same work done at different frequencies"
            ],
            [
                "That's getting closer to the principle! However, it's not just about teams - it's about business requirements. Create separate Time entities when different business domains have fundamentally different timing needs for the same types of work, regardless of organizational structure.",
                "Consistency is valuable! However, forcing all business domains into the same timing pattern often creates inconsistency with business requirements. Real consistency means each domain gets the timing it needs for optimal business outcomes.",
                "Outstanding system thinking! This is exactly how AI-empowered system thinkers approach Time + Worker design. When you hear requirements like 'real-time analytics' and 'daily compliance reports' for similar data, immediately think domain-separated Time entities with shared Worker implementations - pattern recognition that complements AI capabilities."
            ]
        )
        
        # Pause before next experiment
        print("\n" + "="*50)
        self.typewriter_print("🎓 EXPERIMENT 3 COMPLETE!")
        self.typewriter_print("You've mastered domain-separated Time + Worker patterns that serve different business requirements!")
        self.typewriter_print("Next: Discover how systems handle failures gracefully with fault isolation.")
        print()
        input("👤 Press Enter when you're ready for Experiment 4...")
        
        return analytics_final + compliance_final

    def experiment_4_error_handling(self):
        """Experiment 4: Error Handling and Resilience - System fault tolerance"""
        print("\n" + "="*60)
        self.typewriter_print("🛡️ EXPERIMENT 4: ERROR HANDLING AND RESILIENCE")
        print("="*60)
        
        self.typewriter_print("Now you'll see how Time + Worker systems handle failures and maintain resilience.")
        self.typewriter_print("Some Worker tasks will deliberately fail to demonstrate fault isolation.")
        print()
        
        # Create resilient Time entity and Worker building block
        resilient_time_entity = Time("resilient_system")
        resilient_worker = Worker("resilient_processor")
        
        # Track failures for educational purposes
        self.failure_count = 0
        
        # Worker task that sometimes fails
        def unreliable_task(data=None):
            # Ensure some failures occur for demonstration
            if random.random() < 0.4 or self.failure_count < 2:  # 40% failure rate, ensure at least 2 failures
                self.failure_count += 1
                raise Exception(f"Simulated external service failure at {datetime.now().strftime('%H:%M:%S')}")
            
            processing_time = random.uniform(1, 2)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"✅ Unreliable task completed successfully at {datetime.now().strftime('%H:%M:%S')}")
            return {"status": "success", "processing_time": processing_time}
        
        # Worker task that always succeeds
        def reliable_task(data=None):
            processing_time = random.uniform(0.5, 1)
            time.sleep(processing_time)
            with self.print_lock:
                print(f"🟢 Reliable task completed at {datetime.now().strftime('%H:%M:%S')}")
            return {"status": "success", "processing_time": processing_time}
        
        # Register Worker tasks with error handling
        resilient_worker.register_job_type("unreliable_task", unreliable_task)
        resilient_worker.register_job_type("reliable_task", reliable_task)
        
        # Set up Time triggers for Worker tasks
        @resilient_time_entity.recurring_trigger(interval_seconds=4, start_delay=1)
        def trigger_unreliable_work():
            self.direct_print("⚠️  Scheduling unreliable task (might fail)")
            resilient_worker.submit_job("unreliable_task", {})
        
        @resilient_time_entity.recurring_trigger(interval_seconds=3, start_delay=2) 
        def trigger_reliable_work():
            self.direct_print("✅ Scheduling reliable task")
            resilient_worker.submit_job("reliable_task", {})
        
        self.typewriter_print("🧪 Testing Time + Worker system resilience with failing tasks...")
        self.typewriter_print("💪 Observe how the system handles Worker task failures gracefully")
        self.typewriter_print("📈 Notice: Time entity continues triggering despite individual Worker task failures")
        self.typewriter_print("🔄 Observing for 16 seconds...\n")
        
        resilient_time_entity.start_time_monitoring()
        resilient_worker.start()
        
        try:
            start_time = time.time()
            while time.time() - start_time < 16:  # Run for 16 seconds
                elapsed = int(time.time() - start_time)
                stats = resilient_worker.get_stats()
                
                self.direct_print(f"\n💪 Resilient Time + Worker system running... ({elapsed}s elapsed)")
                self.direct_print(f"   ✅ Successful Worker jobs: {stats['completed_jobs']}")
                self.direct_print(f"   ❌ Failed Worker jobs: {stats['failed_jobs']}")
                self.direct_print(f"   📊 Success rate: {stats['success_rate']:.1f}%")
                self.direct_print(f"   🎯 Time entity still operational despite Worker task failures!")
                
                time.sleep(3)
                
        except KeyboardInterrupt:
            self.typewriter_print("\n🛑 Stopping resilient Time + Worker system...")
        
        finally:
            resilient_time_entity.stop_time_monitoring()
            resilient_worker.stop()
            
            final_stats = resilient_worker.get_stats()
            self.typewriter_print(f"\n📊 RESILIENCE TEST SUMMARY:")
            self.typewriter_print(f"   Total Worker jobs attempted: {final_stats['total_jobs']}")
            self.typewriter_print(f"   Successful Worker completions: {final_stats['completed_jobs']}")
            self.typewriter_print(f"   Failed Worker jobs: {final_stats['failed_jobs']}")
            self.typewriter_print(f"   System availability: {final_stats['success_rate']:.1f}%")
            self.typewriter_print(f"   🎯 Time + Worker system remained operational despite {final_stats['failed_jobs']} failures!")
        
        # Multiple choice reflections
        self.ask_multiple_choice(
            "How did the Time + Worker system respond to individual Worker task failures?",
            [
                "The Time entity slowed down to handle failures more carefully",
                "Failed Worker tasks were automatically retried until they succeeded",
                "Failures were isolated and didn't crash the entire Time + Worker system"
            ],
            [
                "That would be a reasonable safety response! However, the Time entity didn't slow down - it continued at normal speed. The key insight is fault isolation: individual Worker task failures don't affect the overall system operation or other tasks. This separation prevents cascading failures.",
                "That would be a helpful feature! However, Worker tasks weren't automatically retried in this demo. The important principle is that individual failures don't crash the entire system. Worker building blocks provide fault isolation so the Time entity continues operating despite individual task problems.",
                "Perfect understanding of resilient architecture! This fault isolation is exactly how Netflix handles millions of operations - individual failures don't bring down the entire platform. This is the difference between code writer and system thinker approaches to system design."
            ]
        )
        
        self.ask_multiple_choice(
            "What would happen in a Time + Worker system without proper fault isolation?",
            [
                "The Time entity would just run more slowly",
                "Failed Worker tasks would be skipped automatically",
                "One Worker failure could crash the entire Time + Worker system"
            ],
            [
                "Running slowly would actually be better than what really happens! Without proper fault isolation, one failing Worker task can bring down the entire Time + Worker system, stopping all automation. This is a common failure mode in systems that need better isolation design.",
                "That would be a nice safety feature! However, without fault isolation, Worker tasks don't get 'skipped' cleanly - they crash the entire system. Worker building blocks provide the boundaries that allow individual Worker tasks to fail safely without affecting the overall Time entity infrastructure.",
                "Exactly right! Without Worker building blocks, one bad task could crash your entire Time + Worker system. This is why system thinkers use proper fault isolation patterns for business-critical reliability."
            ]
        )
        
        self.ask_multiple_choice(
            "How does this resilience apply to real business systems?",
            [
                "Resilience is only important for large tech companies",
                "Most businesses can tolerate system downtime",
                "Business continuity requires systems that work despite individual failures"
            ],
            [
                "That's a common assumption about scale! However, every business - from small e-commerce sites to local service providers - needs resilient systems. Downtime costs money and damages customer trust regardless of company size. Fault isolation benefits all businesses.",
                "Some businesses might seem more tolerant, but system downtime directly impacts revenue, customer satisfaction, and business reputation. Even small businesses benefit greatly from resilient design with fault isolation for business continuity.",
                "Outstanding business thinking! Companies can't afford to shut down when one process fails. Banking systems, e-commerce platforms, and streaming services all use these fault isolation patterns to ensure business operations continue despite individual component failures."
            ]
        )
        
        # Pause before conclusion
        print("\n" + "="*50)
        self.typewriter_print("🎓 EXPERIMENT 4 COMPLETE!")
        self.typewriter_print("You've experienced resilient architecture that handles failures gracefully.")
        self.typewriter_print("Ready for your final transformation summary and course completion.")
        print()
        input("👤 Press Enter when you're ready to complete your journey...")
        
        return final_stats['total_jobs']

    def run_single_experiment(self, experiment_num: int):
        """Run a specific experiment"""
        experiments = {
            1: self.experiment_1_manual_execution,
            2: self.experiment_2_basic_automation,
            3: self.experiment_3_advanced_scheduling,
            4: self.experiment_4_error_handling
        }
        
        if experiment_num in experiments:
            # Simplified welcome for single experiments
            print("\n" + "="*70)
            self.typewriter_print(f"🎯 TIME + WORKER DISCOVERY LAB - EXPERIMENT {experiment_num}")
            print("="*70)
            print()
            
            # Quick name input without full welcome
            self.student_name = input("👤 Enter your name: ").strip()
            if not self.student_name:
                self.student_name = "Explorer"
            
            print()
            self.typewriter_print(f"Welcome {self.student_name}! Starting Experiment {experiment_num} directly.")
            print()
            
            # Run the selected experiment
            experiments[experiment_num]()
            
            # Quick conclusion
            print("\n" + "="*70)
            self.typewriter_print(f"🎉 EXPERIMENT {experiment_num} COMPLETE!")
            print("="*70)
            self.typewriter_print("Great work! Run the complete lab to experience all 4 experiments.")
            print()
        else:
            print(f"Experiment {experiment_num} not found. Available experiments: 1-4")

    def run_complete_lab(self):
        """Run all experiments in sequence"""
        self.welcome()
        
        print()
        self.typewriter_print("🔬 You'll experience 4 progressive experiments:")
        self.typewriter_print("   1. Manual Worker Task Execution - Experience the pain")
        self.typewriter_print("   2. Basic Time + Worker Automation - Feel the relief")
        self.typewriter_print("   3. Advanced Time + Worker Patterns - Multiple Time entities")
        self.typewriter_print("   4. Error Handling and Resilience - System fault tolerance")
        print()
        
        input("👤 Press Enter to begin your discovery journey...")
        
        # Run all experiments
        manual_time = self.experiment_1_manual_execution()
        automated_jobs = self.experiment_2_basic_automation()
        advanced_jobs = self.experiment_3_advanced_scheduling()
        resilience_jobs = self.experiment_4_error_handling()
        
        # Show overall summary
        print("\n" + "="*70)
        self.typewriter_print("🎯 COMPLETE LAB SUMMARY")
        print("="*70)
        
        self.typewriter_print(f"Manual Execution Time: {manual_time:.1f} seconds of waiting")
        self.typewriter_print(f"Automated Jobs Completed: {automated_jobs} (basic automation)")
        self.typewriter_print(f"Advanced Pattern Jobs: {advanced_jobs} (multi-Time entity)")
        self.typewriter_print(f"Resilience Test Jobs: {resilience_jobs} (with failures)")
        
        print()
        self.typewriter_print("🎓 TRANSFORMATION COMPLETE!")
        self.typewriter_print("You've experienced the journey from manual processes to resilient automation.")
        
        self.conclusion()

    def conclusion(self):
        """Wrap up the lab experience"""
        print("\n" + "="*70)
        self.typewriter_print("🎉 CONGRATULATIONS! TIME + WORKER MASTERY ACHIEVED")
        print("="*70)
        
        self.typewriter_print(f"Outstanding work, {self.student_name}!")
        self.typewriter_print("You've discovered the fundamental patterns that power scheduled processing in every modern system.")
        
        print()
        self.typewriter_print("🎯 Key Insights You've Gained:")
        self.typewriter_print("   ⏰ Time entities handle 'when' - providing precise, reliable scheduling")
        self.typewriter_print("   🔧 Worker building blocks handle 'what' - enabling background processing")
        self.typewriter_print("   🏢 Multiple schedulers enable domain separation and independent scaling")
        self.typewriter_print("   🛡️ Fault isolation prevents individual failures from crashing systems")
        
        print()
        self.typewriter_print("🌟 Real-World Applications:")
        self.typewriter_print("   • Netflix billing cycles and content processing")
        self.typewriter_print("   • Instagram photo processing and content moderation")
        self.typewriter_print("   • Banking transactions and fraud detection")
        self.typewriter_print("   • Email marketing campaigns and notifications")
        
        print()
        self.typewriter_print("🚀 You now have the architectural intuition to design systems that:")
        self.typewriter_print("   • Handle time-based business requirements automatically")
        self.typewriter_print("   • Scale without manual intervention")
        self.typewriter_print("   • Remain resilient despite individual component failures")
        self.typewriter_print("   • Enable business growth through reliable automation")
        
        print()
        self.typewriter_print("Continue your Systems Thinking in the AI Era journey to explore more architectural patterns!")
        print()

def main():
    """Main function to run the Time + Worker Discovery Lab"""
    parser = argparse.ArgumentParser(
        description="Lesson 8: Time + Worker - Scheduled Processing Discovery Lab",
        epilog="Examples:\n"
               "  python3 lesson8_interactive_lab.py           # Run complete lab\n"
               "  python3 lesson8_interactive_lab.py 1         # Run experiment 1 only\n"
               "  python3 lesson8_interactive_lab.py 3         # Run experiment 3 only\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'experiment', 
        type=int, 
        nargs='?', 
        choices=[1, 2, 3, 4],
        help='Run a specific experiment (1-4). If not specified, runs complete lab.'
    )
    
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Disable typewriter effect for instant output'
    )
    
    args = parser.parse_args()
    
    lab = TimeWorkerLabExperience(instant_print=args.fast)
    try:
        if args.experiment:
            lab.run_single_experiment(args.experiment)
        else:
            lab.run_complete_lab()
    except KeyboardInterrupt:
        print("\n\n👋 Lab interrupted. Thank you for exploring Time + Worker patterns!")
        print("Run the lab again anytime to continue your discovery journey.")


if __name__ == "__main__":
    main()