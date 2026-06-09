-- Tabla temporal: todo como texto para poder cargar el CSV con valores "unknown"
CREATE TABLE student_data_staging (
    student_id TEXT,
    week TEXT,
    study_hours TEXT,
    sleep_hours TEXT,
    stress_level TEXT,
    attendance_rate TEXT,
    screen_time_hours TEXT,
    caffeine_intake TEXT,
    learning_efficiency TEXT,
    fatigue_index TEXT,
    quiz_score TEXT,
    assignment_score TEXT,
    performance_index TEXT
);

COPY student_data_staging
FROM '/data/raw/student_learning_trajectory_noisy.csv'
DELIMITER ','
CSV HEADER;

-- Tabla definitiva: convertimos a numérico, "unknown" pasa a NULL
CREATE TABLE student_data AS
SELECT
    NULLIF(student_id, 'unknown')::DOUBLE PRECISION AS student_id,
    NULLIF(week, 'unknown')::DOUBLE PRECISION AS week,
    NULLIF(study_hours, 'unknown')::DOUBLE PRECISION AS study_hours,
    NULLIF(sleep_hours, 'unknown')::DOUBLE PRECISION AS sleep_hours,
    NULLIF(stress_level, 'unknown')::DOUBLE PRECISION AS stress_level,
    NULLIF(attendance_rate, 'unknown')::DOUBLE PRECISION AS attendance_rate,
    NULLIF(screen_time_hours, 'unknown')::DOUBLE PRECISION AS screen_time_hours,
    NULLIF(caffeine_intake, 'unknown')::DOUBLE PRECISION AS caffeine_intake,
    NULLIF(learning_efficiency, 'unknown')::DOUBLE PRECISION AS learning_efficiency,
    NULLIF(fatigue_index, 'unknown')::DOUBLE PRECISION AS fatigue_index,
    NULLIF(quiz_score, 'unknown')::DOUBLE PRECISION AS quiz_score,
    NULLIF(assignment_score, 'unknown')::DOUBLE PRECISION AS assignment_score,
    NULLIF(performance_index, 'unknown')::DOUBLE PRECISION AS performance_index
FROM student_data_staging;

DROP TABLE student_data_staging;
