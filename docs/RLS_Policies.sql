ALTER TABLE enrollment ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempt ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_answer ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignment_submission ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY student_enrollment_policy
ON enrollment
FOR SELECT
USING (student_id = current_setting('app.current_student_id'));

CREATE POLICY student_quiz_attempt_policy
ON quiz_attempt
FOR SELECT
USING (student_id = current_setting('app.current_student_id'));

CREATE POLICY student_quiz_answer_policy
ON quiz_answer
FOR SELECT
USING (
    attempt_id IN (
        SELECT id FROM quiz_attempt WHERE student_id = current_setting('app.current_student_id')
    )
);

CREATE POLICY student_assignment_submission_policy
ON assignment_submission
FOR SELECT
USING (student_id = current_setting('app.current_student_id'));

CREATE POLICY student_progress_policy
ON student_progress
FOR SELECT
USING (student_id = current_setting('app.current_student_id'));


CREATE POLICY instructor_enrollment_policy
ON enrollment
FOR SELECT
USING (
    course_id IN (
        SELECT id FROM course WHERE instructor_id = current_setting('app.current_instructor_id')
    )
);

CREATE POLICY instructor_assignment_submission_policy
ON assignment_submission
FOR SELECT
USING (
    assignment_id IN (
        SELECT id FROM assignment WHERE course_id IN (
            SELECT id FROM course WHERE instructor_id = current_setting('app.current_instructor_id')
        )
    )
);

CREATE POLICY instructor_quiz_attempt_policy
ON quiz_attempt
FOR SELECT
USING (
    quiz_id IN (
        SELECT id FROM quiz WHERE course_id IN (
            SELECT id FROM course WHERE instructor_id = current_setting('app.current_instructor_id')
        )
    )
);


CREATE POLICY admin_policy_enrollment
ON enrollment
FOR ALL
USING (current_setting('app.current_role') = 'administrator');

CREATE POLICY admin_policy_quiz_attempt
ON quiz_attempt
FOR ALL
USING (current_setting('app.current_role') = 'administrator');

CREATE POLICY admin_policy_assignment_submission
ON assignment_submission
FOR ALL
USING (current_setting('app.current_role') = 'administrator');

CREATE POLICY admin_policy_student_progress
ON student_progress
FOR ALL
USING (current_setting('app.current_role') = 'administrator');


SET app.current_role = 'student';
SET app.current_student_id = 'uuid-of-student';


#Trigger
CREATE OR REPLACE FUNCTION update_quiz_average()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE student_progress
    SET quiz_average = (
        SELECT AVG(score)
        FROM quiz_attempt
        WHERE student_id = NEW.student_id
          AND course_id = (SELECT course_id FROM quiz WHERE id = NEW.quiz_id)
    )
    WHERE student_id = NEW.student_id
      AND course_id = (SELECT course_id FROM quiz WHERE id = NEW.quiz_id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_quiz_average
AFTER INSERT OR UPDATE ON quiz_attempt
FOR EACH ROW
EXECUTE FUNCTION update_quiz_average();


CREATE OR REPLACE FUNCTION update_assignment_average()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE student_progress
    SET assignment_average = (
        SELECT AVG(score)
        FROM assignment_submission
        WHERE student_id = NEW.student_id
          AND assignment_id IN (
              SELECT id FROM assignment WHERE course_id = (
                  SELECT course_id FROM assignment WHERE id = NEW.assignment_id
              )
          )
    )
    WHERE student_id = NEW.student_id
      AND course_id = (
          SELECT course_id FROM assignment WHERE id = NEW.assignment_id
      );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_assignment_average
AFTER INSERT OR UPDATE ON assignment_submission
FOR EACH ROW
EXECUTE FUNCTION update_assignment_average();

#Auto-update enrollment.progress when lessons are completed
CREATE OR REPLACE FUNCTION update_course_progress()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE enrollment
    SET progress = progress + 1
    WHERE student_id = NEW.student_id
      AND course_id = NEW.course_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_course_progress
AFTER INSERT ON student_progress
FOR EACH ROW
EXECUTE FUNCTION update_course_progress();
