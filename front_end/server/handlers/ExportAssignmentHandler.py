from BaseUserHandler import *

class ExportAssignmentHandler(BaseUserHandler):
    def get(self, course, assignment):
        json_text = "An unknown error occurred."

        try:
            if self.is_administrator() or self.is_instructor_for_course(course):
                assignment_basics = self.content.get_assignment_basics(course, assignment)
                del assignment_basics["id"]
                del assignment_basics["exists"]
                del assignment_basics["course"]

                assignment_details = self.content.get_assignment_details(course, assignment)

                exercises = {}
                for exercise_id in self.content.get_exercise_ids(course, assignment):
                    exercise_basics = self.content.get_exercise_basics(course, assignment, exercise_id)
                    del exercise_basics["id"]
                    del exercise_basics["exists"]
                    del exercise_basics["assignment"]

                    exercise_details = self.content.get_exercise_details(course, assignment, exercise_id)
                    for test_title in exercise_details["tests"]:
                        del exercise_details["tests"][test_title]["test_id"]

                    exercises[exercise_basics["title"]] = {"basics": exercise_basics, "details": exercise_details}

                assignment_dict = {
                    "version": read_file('../VERSION').rstrip("\n"),
                    "basics": assignment_basics,
                    "details": assignment_details,
                    "exercises": exercises
                }

                json_text = json.dumps(assignment_dict, default=str)
            else:
                json_text += " You do not have permission to perform this operation."
        except Exception as inst:
            json_text += " " + traceback.format_exc()

        self.set_header('Content-type', "application/json")
        self.write(json_text)
        self.finish()
