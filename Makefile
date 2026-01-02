TEST_DIR := tests
DATA_DIR := data
LOG_DIR  := logs

.PHONY: setup tests clean

# Default
setup: tests
	@echo "Test environment created."

# Create test files and directories with various permissions
tests:
	@echo "Creating test directories and files..."

# Create directories
	mkdir -p $(TEST_DIR)/subdir
	mkdir -p $(DATA_DIR)
	mkdir -p $(LOG_DIR)

# Create files
	echo "read only file" > $(TEST_DIR)/file_read_only.txt
	echo "write only file" > $(TEST_DIR)/file_write_only.txt
	echo "executable file" > $(TEST_DIR)/file_exec.sh
	echo "all permissions file" > $(TEST_DIR)/file_all_perms.txt
	echo "nested file" > $(TEST_DIR)/subdir/nested_file.txt
	echo "sticky file" > $(TEST_DIR)/subdir/sticky_file.txt

# Set permissions
	chmod 444 $(TEST_DIR)/file_read_only.txt
	chmod 222 $(TEST_DIR)/file_write_only.txt
	chmod 755 $(TEST_DIR)/file_exec.sh
	chmod 777 $(TEST_DIR)/file_all_perms.txt
	chmod 644 $(TEST_DIR)/subdir/nested_file.txt

# Set sticky bit on file
	chmod 1755 $(TEST_DIR)/subdir/sticky_file.txt

	@echo "Permissions applied:"
	@ls -lR $(TEST_DIR)

# Clean generated files and directories
clean:
	@echo "Cleaning project..."
	rm -rf $(TEST_DIR)
	rm -rf $(DATA_DIR)
	rm -rf $(LOG_DIR)
	@echo "Cleanup complete."
