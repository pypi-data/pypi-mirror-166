from datetime import datetime
from threading import Thread
from frelatage.config.config import Config


def fuzz(self) -> None:
    """
    Run the fuzzer
    """
    # Initialize the fuzzer timer
    self.fuzz_start_time = datetime.now()

    # Initialize file input folders in /tmp/frelatage (default value)
    # Can be modified using the FRELATAGE_INPUT_FILE_TMP_DIR env variable
    self.init_file_inputs()

    # Infinite fuzzing is allowed if we have one input combination
    if self.infinite_fuzz and len(self.queue.arguments) > 1:
        print("Error: infinite fuzzing is only possible with a corpus of size 1")
        exit(1)

    try:
        # Interface
        if not self.silent:
            p = Thread(target=self.start_interface)
            p.daemon = True
            p.start()

        # Fuzzing
        parents = [self.arguments]
        while True:
            self.generate_cycle_mutations(parents)
            reports = self.run_cycle()
            # If no new paths have been found for a while, we go to the next stage
            if (
                self.cycles_without_new_path
                >= Config.FRELATAGE_MAX_CYCLES_WITHOUT_NEW_PATHS
                and not self.infinite_fuzz
            ):
                # Next stage
                self.queue.position += 1
                if not self.queue.end:
                    # Initialize the new stage
                    self.arguments = self.queue.current_arguments()
                    parents = [self.arguments]
                    self.cycles_without_new_path = 0
                    self.stage_inputs_count = 0
                    self.init_file_inputs()
                # End of the fuzzing process
                # Exit the program
                else:
                    if self.report:
                        self.exit_message(normal_ending=True)
                        exit(1)
                    self.alive = False
                    self.kill_interface()
                    break
            else:
                parents = self.evaluate_mutations(reports)
    # Exit the program
    # Keyboard interrupt
    except KeyboardInterrupt:
        self.exit_message(aborted_by_user=True)
        exit(0)
    # Error in Frelatage
    except Exception as e:
        self.exit_message(aborted_by_user=False)
        if Config.FRELATAGE_DEBUG_MODE:
            print(e)
        exit(1)
