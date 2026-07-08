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
