class helper:
    @staticmethod
    def inference_helper(inference) -> dict:
        return {
            "id": str(inference["_id"]),
            "ms_circle_arm": inference["ms_circle_arm"],
            "ms_frontal_arm": inference["ms_frontal_arm"],
            "ms_no_movement": inference["ms_no_movement"],
            "ms_side_arm": inference["ms_side_arm"],
            "ms_upper_arm": inference["ms_upper_arm"],
            "created_at": inference["created_at"],
        }
