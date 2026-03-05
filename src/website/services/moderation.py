import re

from better_profanity import profanity

from src.core.constants.review import ModerationStatus


class ReviewModerationService:
    URL_REGEX = re.compile(
        r"(https?://|www\.)[^\s]+",
        re.IGNORECASE
    )

    @staticmethod
    def contains_link(text: str) -> bool:
        return bool(ReviewModerationService.URL_REGEX.search(text))

    @staticmethod
    def normalize(text: str) -> str:
        return text.lower().strip()

    @classmethod
    def moderate(cls, review):
        text = cls.normalize(f"{review.title} {review.text}")

        if profanity.contains_profanity(text) or cls.contains_link(text):
            review.moderation_status = ModerationStatus.PENDING
        else:
            review.moderation_status = ModerationStatus.APPROVED

        review.save(update_fields=["moderation_status"])
