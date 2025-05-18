
-- Створення таблиці employees.
CREATE TABLE employees_20 (
    employee_id INT,
    name VARCHAR(100),
    job_id INT,
    salary INT,
    department_id INT,
    hire_date DATE
);


-- Запис випадкових даних у таблицю employees.
INSERT INTO public.employees_20 (employee_id, name, job_id, salary, department_id, hire_date) VALUES
(1, 'John Doe', 101, 60000, 1, '2022-01-01'),
(2, 'Jane Smith', 102, 100000, 1, '2022-02-15'),
(3, 'Bob Johnson', 103, 75000, 2, '2022-03-10'),
(4, 'Alice Brown', 104, 48000, 6, '2022-04-20'),
(5, 'Michael Green', 105, 45000, 10, '2021-05-18'),
(6, 'Emma Wilson', 106, 38000, 3, '2021-06-12'),
(7, 'David Lee', 107, 60000, 8, '2021-07-07'),
(8, 'Olivia Harris', 108, 42000, 8, '2021-08-03'),
(9, 'Daniel Adams', 109, 46000, 6, '2022-09-27'),
(10, 'Sophia Turner', 110, 91000, 10, '2022-10-14');


-- Створення таблиці departments.
CREATE TABLE departments_20 (
    department_id INT,
    department_name VARCHAR(100)
);


-- Запис випадкових даних у таблицю departments.
INSERT INTO departments_20 (department_id, department_name) VALUES
(1, 'IT'),
(2, 'Finance'),
(3, 'Human Resources'),
(6, 'Marketing'),
(8, 'Sales'),
(10, 'Customer Support');


-- Завдання 1. Вивести всі дані з таблиці "employees".			
SELECT * FROM employees_20;


-- Завдання 2. Вибрати імена та зарплати всіх працівників, які отримують більше 50000.				
SELECT * FROM employees_20 WHERE salary > 50000;


-- Завдання 3. Знайти кількість працівників в департаменті з ідентифікатором 10.
SELECT COUNT(*) AS employee_count
FROM public.employees_20
WHERE department_id = 10;

-- Завдання 4. Вивести унікальні департаменти в яких працюють працівники з таблиці "departments".
SELECT DISTINCT d.department_id, d.department_name
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id;

SELECT DISTINCT d.department_id, d.department_name
FROM public.departments_20 d;


-- Завдання 5. Вивести загальну кількість працівників в кожному департаменті та середню зарплату.		
SELECT 
    d.department_name,
    COUNT(*) AS employee_count,
    AVG(e.salary) AS average_salary
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_salary DESC;


-- Завдання 6. Знайти працівника з найвищою зарплатою та вказати назву його департаменту department_name.		
SELECT 
    e.name AS employee_name,
    e.salary AS highest_salary,
    d.department_name
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id
ORDER BY e.salary DESC
LIMIT 1;


--Завдання 7. Вивести загальну суму зарплат у кожному департаменті та відсортувати в порядку спадання.		
SELECT 
    d.department_name,
    SUM(e.salary) AS total_salary
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_salary DESC;


-- Завдання 8. Знайти середню зарплату для працівників, найманих після 1 січня 2022 року.
SELECT 
    AVG(e.salary) AS average_salary
FROM public.employees_20 e
WHERE e.hire_date > '2022-01-01';


-- Завдання 9. Вивести топ-3 департаменти з найвищою середньою зарплатою.	
SELECT
    d.department_name,
    AVG(e.salary) AS highest_average_salary
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY highest_average_salary DESC
LIMIT 3;


-- Завдання 10. Вивести назву департаменту з другою найбільшою середньою зарплатнею.
SELECT
    d.department_name,
    AVG(e.salary) AS highest_average_salary
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY highest_average_salary DESC
LIMIT 1
OFFSET 1;


-- Завдання 11. Вибрати імена працівників, які мають унікальні зарплати та працюють в IT-відділі.
SELECT 
    e.name AS employee_name,
    e.salary,
    d.department_name
FROM public.employees_20 e
JOIN public.departments_20 d ON e.department_id = d.department_id
WHERE d.department_name = 'IT'
AND e.salary IN (
    SELECT salary
    FROM public.employees_20
    GROUP BY salary
    HAVING COUNT(*) = 1
)
ORDER BY e.salary DESC;



