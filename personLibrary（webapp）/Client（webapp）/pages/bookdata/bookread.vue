<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">  
		    <view class="top_view"></view>  
		</view>  
		<!-- #endif -->
		<view style="height: 50upx;">
			<view @tap="gobookdata(book.wbookid)" class="cuIcon-back cu-btn" style="padding-left: 10upx;">
				返回详情页
			</view>
		</view>
		<view style="width: 700upx;padding: 10upx 0 20upx 20upx;border: 1px solid #e0e0e0;">
			<view style="">{{bookdata}}</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				bookdata: "",
				book: ""
			}
		},
		methods: {
			gobookdata(id) {
				var data = "";
				var book_content = "";
				uni.showModal({
					title: '提示',
					content: '返回详情页?',
					success: function(res) {
						if (res.confirm == true) {
							uni.navigateTo({
								url: `../bookdata/bookdata?id=${id}`,
								animationType:"zoom-fade-out",
								animationDuration:500
							})
						} else if (res.cancel == true) {

						}

					},
				})
			},
			get_book() {
				var data = "";
				try {
					const res = uni.getStorageSync('bookim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				};
				if (data != "") {
					this.bookdata = data.bookdata;
					this.book = data.book;
				} else {
					uni.showToast({
						icon: "none",
						title: "读取失败"
					})
				}
			}


		},
		onLoad() {
			this.get_book();
		}
	}
</script>

<style>
	.status_bar {
	    height: var(--status-bar-height);  
	    width: 100%;  
	    background-color: #F8F8F8;  
	}  
	.top_view {  
	    height: var(--status-bar-height);  
	    width: 100%;  
	    position: fixed;  
	    background-color: #F8F8F8;  
	    top: 0;  
	    z-index: 999;  
	}
</style>
