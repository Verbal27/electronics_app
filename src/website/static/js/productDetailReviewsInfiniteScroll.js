function initReviewsInfiniteScroll(options = {}) {
    const {
        containerSelector = '#reviews-container',
        sentinelSelector = '#sentinel',
        loadingSelector = '#loading',
        url,
        initialPage
    } = options;

    let page = initialPage;
    let loading = false;
    let hasNext = true;

    const container = document.querySelector(containerSelector);
    const sentinel = document.querySelector(sentinelSelector);
    const loadingIndicator = document.querySelector(loadingSelector);

    if (!container || !sentinel || !loadingIndicator || !url) {
        console.warn('Infinite scroll: Required elements not found.');
        return;
    }

    const loadMoreReviews = async () => {
        if (loading || !hasNext) return;

        loading = true;
        loadingIndicator.classList.remove('d-none');

        try {
            const response = await fetch(`${url}?page=${page}`, {
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();

            sentinel.insertAdjacentHTML('beforebegin', data.html);

            hasNext = data.has_next;
            page += 1;

            if (hasNext) {
                observer.observe(sentinel);
            }
        } catch (error) {
            console.error('Failed to load more reviews:', error);
        } finally {
            loading = false;
            loadingIndicator.classList.add('d-none');
        }
    };

    const observer = new IntersectionObserver(entries => {
        if (!entries[0].isIntersecting || loading || !hasNext) return;
        loadMoreReviews();
    }, {
        root: container,
        rootMargin: '200px',
        threshold: 0
    });

    observer.observe(sentinel);
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('#reviews-container');
    if (!container) return;

    const url = container.dataset.infiniteUrl;
    const nextPage = container.dataset.nextPage;

    if (!nextPage) return;

    const initialPage = parseInt(nextPage);


    initReviewsInfiniteScroll({
        url: url,
        containerSelector: '#reviews-container',
        sentinelSelector: '#sentinel',
        loadingSelector: '#loading',
        initialPage: initialPage
    });
});