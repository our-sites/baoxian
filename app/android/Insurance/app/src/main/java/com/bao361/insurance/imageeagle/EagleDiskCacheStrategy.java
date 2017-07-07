package com.bao361.insurance.imageeagle;

/**
 * 缓存策略
 */
public enum EagleDiskCacheStrategy {
    /** Caches with both {@link #SOURCE} and {@link #RESULT}. */
    ALL(true, true),
    /** Saves no data to cache. */
    NONE(false, false),
    /** Saves just the original data to cache. */
    SOURCE(true, false),
    /** Saves the media item after all transformations to cache. */
    RESULT(false, true);

    private final boolean cacheSource;
    private final boolean cacheResult;

    EagleDiskCacheStrategy(boolean cacheSource, boolean cacheResult) {
        this.cacheSource = cacheSource;
        this.cacheResult = cacheResult;
    }

    /**
     * Returns true if this request should cache the original unmodified data.
     */
    public boolean cacheSource() {
        return cacheSource;
    }

    /**
     * Returns true if this request should cache the final transformed result.
     */
    public boolean cacheResult() {
        return cacheResult;
    }
}
