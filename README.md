# File Monitoring Tool

**Operating Systems – Project Report**

---

## 1. Introduction

This project implements a **Linux-based file monitoring tool** developed for my **Operating Systems** course.

The goal of the tool is to monitor files and directories for changes in their properties, detect potential security issues, and allow administrators to manage file access permissions. The system continuously monitors selected paths, logs detected events for later analysis, and verifies file integrity using cryptographic hashes.

The tool is implemented in **Python**, leveraging Linux system calls through the Python standard library, and focuses on operating system concepts such as file metadata, permissions, ownership, and data integrity.

---

## 2. System Architecture

The project follows a **modular architecture**, where each component has a clearly defined responsibility. 

### 2.1 High-Level Architecture

```
+------------------+
|     main.py      |
|  (CLI Interface) |
+--------+---------+
         |
         v
+--------+---------+
|   monitor.py     |
|  (Detection &    |
|   Integrity)     |
+--------+---------+
         |
         v
+--------+---------+
|   storage.py     |
| (State & Files)  |
+--------+---------+
         |
         v
+--------+---------+
| permissions.py  |
| (Access Rights) |
+-----------------+

+-----------------+
|    utils.py     |
| (Helpers & Log) |
+-----------------+
```

---

### 2.2 Component Description

#### `main.py`

**Program entry point and user interface**

Responsibilities:

* Implements the command-line interface (CLI)
* Parses user commands
* Controls program flow
* Starts single or continuous monitoring scans
* Delegates work to other modules

---

#### `monitor.py`

**Monitoring and detection logic**

Responsibilities:

* Collect file metadata (size, permissions, ownership, timestamps)
* Compute cryptographic hashes for integrity checking
* Compare current metadata with stored baseline data
* Make necessary changes to stored data as files are modified
* Log file modification events

Key functions:

* `get_file_metadata(path)`
* `scan_once(monitored_files)`

---

#### `storage.py`

**Monitoring state and persistence**

Responsibilities:

* Store metadata for monitored files
* Maintain the list of monitored paths
* Add and remove files or directories (recursive or non-recursive)
* Save and load monitoring state using JSON

---

#### `permissions.py`

**Access rights management**

Responsibilities:

* Retrieve file permissions in human-readable and octal formats
* Modify permissions using readable English words
* Support special permission bits (SUID, SGID, sticky bit)

Key functions:

* `get_permissions_str(path)`
* `modify_permission(path, entity, perms, action)`

---

#### `utils.py`

**Helper utilities**

Responsibilities:

* Event classification (severity levels)
* Event formatting for display and logging
* Logging setup and shared helper logic
* Code reuse across modules

---

## 3. Implemented Features

### 3.1 File Property Monitoring

The tool monitors the following file properties:

* File size
* Access permissions
* Ownership (user and group)
* Modification timestamps
* Cryptographic file hash

Changes are detected by periodically scanning monitored paths and comparing current metadata against stored baseline values. Non-readable files are skipped for the hashing and are denote by UNREADABLE in the metadata.

---

### 3.2 Continuous Monitoring

The system supports a **continuous monitoring mode**, where scans are performed at regular intervals (default interval of 5 seconds) until the program is manually stopped.

---

### 3.3 Adding and Removing Files or Directories

Users can:

* Add individual files to the monitoring list
* Add directories, with optional recursive traversal
* Remove monitored files or directories

---

### 3.4 Access Rights Management

The tool allows administrators to modify permissions using **readable English words**, such as:

* Read
* Write
* Execute

Permissions can be applied to:

* User
* Group
* Others
* All entities
* Special bits (SUID, SGID, sticky bit)

Permissions can be viewed and modified in:

* Human-readable format (e.g. `-rwxr-xr--`)
* Octal format (e.g. `0755`)

---

### 3.5 Data Security and Integrity

To ensure data integrity:

* A cryptographic hash is calculated for each monitored file
* Hash changes indicate modifications to file contents
* Integrity violations are logged as high-severity events

This mechanism helps detect unauthorized or unexpected file modifications.

---

### 3.6 Logging and Event Reporting

All detected events are logged with:

* Timestamp
* Severity level
* Description of the change

Logs are stored in a log file (`file_monitor.log`) for later analysis.

---

## 4. Security Testing and Results

### 4.1 Test Scenarios

| Test Case                       | Expected Result          | Outcome |
| ------------------------------- | ------------------------ | ------- |
| Modify file content             | Hash change detected     | Passed  |
| Change file permissions         | Permission change logged | Passed  |
| Change file ownership           | Ownership change logged  | Passed  |
| Recursive directory monitoring  | All files detected       | Passed  |
| Continuous monitoring stability | No crashes               | Passed  |

---

### 4.2 Observations

* Hash-based integrity checks reliably detect content changes
* Metadata changes are correctly identified and logged
* Permission modifications are accurately applied
* Continuous monitoring remains stable during execution
* Multiple instances of the program can run, but only the 1st instance can modify the metadata

---

## 5. Limitations

* Monitoring relies on periodic polling instead of kernel event notifications
* Large directories may increase scan time
* No authentication or role separation within the CLI
* Graphical user interface (GUI) is not implemented

---

## 6. Recommendations for Improving Robustness

* Integrate Linux `inotify` for real-time event detection
* Optimize performance by reducing unnecessary hash recalculations (by caching)
* Add role-based access control (like logging in for admin)
* Convert the tool into a background daemon
* Implement a graphical user interface
* Improve crash recovery and error handling

---

## 7. How to Run the Project

From the **project root directory**:

```bash
python -m src.main
```

Inputs:

1. List monitored files
2. Add/remove a file from monitoring
3. Add/remove a directory from monitoring
4. Scan monitored files once
5. Change file permissions
6. Get file permissions
7. Start continuous scanning
8. Exit

---

## 7.1 Testing

A Makefile was created to test certain scenarios and file types.

From the **project root**:
```bash
make tests
```

```bash
make clean
```

---

## 8. Conclusion

This project demonstrates the implementation of a Linux file monitoring system that integrates key operating system concepts such as file metadata management, access rights control, and data integrity verification. The modular architecture allows for future extensions and improvements, making the tool a solid foundation for secure file monitoring.

---

## 9. References

* Linux `stat` system call documentation
* Python Standard Library (`os`, `stat`, `hashlib`, `pathlib`)
* Linux filesystem permissions documentation

