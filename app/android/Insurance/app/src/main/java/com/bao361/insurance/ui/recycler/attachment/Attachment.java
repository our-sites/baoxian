package com.bao361.insurance.ui.recycler.attachment;

import android.content.Context;

import com.bao361.insurance.ui.recycler.holders.AttachmentViewHolder;

import java.util.ArrayList;

/**
 * Adapter 的附件, 用于挂载 Header和Footer
 */
public class Attachment {
    public static final int HEADERS_START = Integer.MIN_VALUE;
    public static final int FOOTERS_START = HEADERS_START + 10000;

    private final Context mContext;

    private ArrayList<AttachmentViewHolder> mHeaders = new ArrayList<>();
    private ArrayList<AttachmentViewHolder> mFooters = new ArrayList<>();

    public Attachment(Context context) {
        this.mContext = context;
    }

    public Context getContext() {
        return mContext;
    }

    public void addHeader(AttachmentViewHolder vhHeader) {
        if (vhHeader == null) {
            return;
        }
        this.mHeaders.add(vhHeader);
    }

    public void addFooter(AttachmentViewHolder vhFooter) {
        if (vhFooter == null) {
            return;
        }
        this.mFooters.add(vhFooter);
    }

    public void removeHeader(AttachmentViewHolder vhHeader) {
        if (vhHeader == null) {
            return;
        }
        this.mHeaders.remove(vhHeader);
    }

    public void removeFooter(AttachmentViewHolder vhFooter) {
        if (vhFooter == null) {
            return;
        }
        this.mFooters.remove(vhFooter);
    }

    public AttachmentViewHolder getHeader(int index) {
        if (index >= getHeaderCount()) {
            return null;
        }
        return this.mHeaders.get(index);
    }

    public AttachmentViewHolder getFooter(int index) {
        if (index >= getFooterCount()) {
            return null;
        }
        return this.mFooters.get(index);
    }

    public int getItemViewType(int position, int itemCount) {
        if (isHeader(position)) {
            return HEADERS_START + position;
        } else {
            int fIndex = position - getHeaderCount() - itemCount;
            return FOOTERS_START + fIndex;
        }
    }

    public AttachmentViewHolder getItemViewHolder(int viewType) {
        if (viewType < FOOTERS_START) { // get header
            int fIndex = viewType - HEADERS_START;
            if (fIndex >= getHeaderCount()) {
                return null;
            }
            return this.mHeaders.get(fIndex);
        } else { // get footer
            int fIndex = viewType - FOOTERS_START;
            if (fIndex >= getFooterCount()) {
                return null;
            }
            return this.mFooters.get(fIndex);
        }
    }

    public int getHeaderCount() {
        return mHeaders.size();
    }

    public int getFooterCount() {
        return mFooters.size();
    }

    public int getCount() {
        return getHeaderCount() + getFooterCount();
    }

    public boolean isAttachment(int position, int itemCount) {
        return isHeader(position) || isFooter(position, itemCount);
    }

    public boolean isAttachmentType(int type) {
        return isHeaderType(type) || isFooterType(type);
    }

    public boolean isHeader(int position) {
        return position < getHeaderCount();
    }

    public boolean isHeaderType(int type) {
        return /*type >= HEADERS_START && */type < HEADERS_START + getHeaderCount();
    }

    public boolean isFooter(int position, int itemCount) {
        return getHeaderCount() + itemCount == 0 || position > getHeaderCount() + itemCount - 1;
    }

    public boolean isFooterType(int type) {
        return type >= FOOTERS_START && type < FOOTERS_START + getFooterCount();
    }

}
