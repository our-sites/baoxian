package com.bao361.insurance.ui.recycler.attachment;

import android.content.Context;
import android.view.View;

import com.bao361.insurance.ui.recycler.holders.AttachmentViewHolder;


/**
 * Adapter 的附件, 用于挂载 Header和Footer
 */
public class AttachmentGroup extends Attachment {

    private AttachmentViewHolder mHeaderGroup;
    private AttachmentViewHolder mFooterGroup;

    /**
     * 默认的Header和Footer group,
     */
    private static class StaticGroup extends AttachmentViewHolder {
        public StaticGroup(Context context) {
            super(context, new View(context));
        }

        @Override
        protected void onViewCreated(View itemView) {
        }

        @Override
        public void onBindViewHolder(int position) {
        }

        @Override
        public void onItemClick(int position) {
        }
    }

    public AttachmentGroup(Context context) {
        super(context);
    }

    public void setHeaderGroup(AttachmentViewHolder headerGroup) {
        this.mHeaderGroup = headerGroup;
    }

    public void setFooterGroup(AttachmentViewHolder footerGroup) {
        this.mFooterGroup = footerGroup;
    }

    public AttachmentViewHolder getHeaderGroup() {
        if (mHeaderGroup == null) {
            mHeaderGroup = new StaticGroup(getContext());
        }
        return mHeaderGroup;
    }

    public AttachmentViewHolder getFooterGroup() {
        if (mFooterGroup == null) {
            mFooterGroup = new StaticGroup(getContext());
        }
        return mFooterGroup;
    }

    @Override
    public AttachmentViewHolder getItemViewHolder(int viewType) {
        if (viewType == HEADERS_START) {
            return getHeaderGroup();
        } else if (viewType == FOOTERS_START) {
            return getFooterGroup();
        } else {
            return super.getItemViewHolder(viewType - 1); // - 1 header group | footer group
        }
    }

    @Override
    public int getHeaderCount() {
        int count = super.getHeaderCount();
        return count == 0 ? count : count + 1;
    }

    @Override
    public int getFooterCount() {
        int count = super.getFooterCount();
        return count == 0 ? count : count + 1;
    }


}
