import re

from better_profanity import profanity

from src.core.constants.review import ProductReviewStatus


class ProductReviewModerationService:
    URL_REGEX = re.compile(
        r"(https?://|www\.)[^\s]+",
        re.IGNORECASE
    )

    @staticmethod
    def contains_link(text: str) -> bool:
        return bool(ProductReviewModerationService.URL_REGEX.search(text))

    @staticmethod
    def normalize(text: str) -> str:
        return text.lower().strip()

    @classmethod
    def moderate(cls, review):
        text = cls.normalize(f"{review.title} {review.text}")

        if profanity.contains_profanity(text) or cls.contains_link(text):
            review.moderation_status = ProductReviewStatus.PENDING
        else:
            review.moderation_status = ProductReviewStatus.APPROVED

        review.save(update_fields=["moderation_status"])
