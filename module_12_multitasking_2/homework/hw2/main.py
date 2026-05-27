import subprocess


def process_count(username: str) -> int:
    """
    Возвращает количество процессов, запущенных пользователем username.
    Использует ps -u --no-headers для фильтрации.
    """
    try:
        output = subprocess.check_output(
            ["ps", "-u", username, "--no-headers"],
        )
        return len(output.decode().strip().splitlines())
    except subprocess.CalledProcessError:
        return 0


def total_memory_usage(root_pid: int) -> float:
    """
    Возвращает суммарное потребление памяти древа процессов с корнем root_pid в %.
    """
    try:
        # Получаем память корня
        root_mem = subprocess.check_output(
            ["ps", "-p", str(root_pid), "-o", "pmem=", "--no-headers"]
        )
        total_mem = float(root_mem.decode().strip())

        # Рекурсивно добавляем память всех потомков (итеративно, без рекурсии)
        pids_to_check = [root_pid]
        checked = set()

        while pids_to_check:
            pid = pids_to_check.pop()
            if pid in checked:
                continue
            checked.add(pid)

            # Получаем прямых потомков через pgrep
            try:
                children = subprocess.check_output(
                    ["pgrep", "-P", str(pid)],
                ).decode().split()
                pids_to_check.extend(children)
            except subprocess.CalledProcessError:
                pass

        # Добавляем память потомков
        for pid in checked:
            if pid == root_pid:
                continue
            try:
                mem = subprocess.check_output(
                    ["ps", "-p", str(pid), "-o", "pmem=", "--no-headers"]
                )
                total_mem += float(mem.decode().strip())
            except subprocess.CalledProcessError:
                continue

        return round(total_mem, 2)
    except Exception:
        return 0.0


if __name__ == "__main__":
    print(f"Процессов пользователя denis: {process_count('denis')}")
    print(f"Память дерева процесса 1: {total_memory_usage(1)}%")