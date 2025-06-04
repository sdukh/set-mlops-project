#!/usr/bin/env python3
"""
Демонстрація прямого підключення до Ray кластера
Запуск: python direct_ray_demo.py
"""

import ray
import time
import random

print("🚀 Демонстрація прямого підключення до Ray кластера")

# Підключаємося до Ray кластера через зовнішню адресу
print("📡 Підключення до Ray кластера...")
ray.init(address="ray://localhost:10001")

print(f"✅ Підключено до кластера: {ray.cluster_resources()}")

# Визначаємо просту remote функцію
@ray.remote
def compute_task(x):
    """Проста обчислювальна задача"""
    time.sleep(random.uniform(1, 3))  # Симулюємо роботу
    result = x * x + random.randint(1, 100)
    print(f"🔢 Обчислено: {x} -> {result}")
    return result

# Запускаємо кілька задач
print("🎯 Запуск задач...")
futures = [compute_task.remote(i) for i in range(5)]

# Отримуємо результати
print("⏳ Очікування результатів...")
results = ray.get(futures)

print(f"✨ Результати: {results}")
print("🎉 Демонстрація завершена!")

ray.shutdown()

if __name__ == "__main__":
    main() 