<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="book_read_top">
			<text>我的收藏</text>
		</view>
		<view class="book_read_rest">
			<view class="book-img-item">
				<image @tap="goaddbook()" :src="book_add_img[0].url"></image>
				<button @tap="goaddbook()" class="bg-gradual-red" style="width: 200upx;height: 50upx;font-size: 80%;font-weight: bold;">{{book_add_img[0].name}}</button>
			</view>
			<view v-for="(item,index) in likebook" :key="index"
			 class="book-img-item">
				<image @tap="gotodetail(item.data[0].wbookid,item.data[0].wbookname)" :src="item.data[0].wbookimage"></image>
				<!-- <view style="text-align: center;">
						{{item.wbookname}}
					</view> -->
				<view>
					<button @tap="godelbook(item.data[0].wbookid,item.data[0].wbookname)" class="bg-gradual-red" style="width: 200upx;height: 50upx;font-size: 80%;font-weight: bold;">移除本书</button>
				</view>
			</view>
		</view>
		
	</view>
	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				text: 'uni-app',
				book_add_img: [],
				wusername: "",
				likebook: ""

			}
		},
		onLoad() {
			this.getbookimg();
			this.getlike();
			setTimeout(function() {
			}, 1000);
			//uni.startPullDownRefresh();
			uni.startPullDownRefresh({
				success: function(res) {//success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画

		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.getlike();
		},
		onReady() {

		},
		methods: {
			godelbook(id, name) {
				var bookname_1 = name;
				var data = "";
				uni.showModal({
					title: '提示',
					content: '是否删除?',
					success: function(res) {
						if (res.confirm == true) {
							try {
								const res = uni.getStorageSync('userim');
								data = JSON.parse(res);
								this.wusername = data.wusername;
							} catch (e) {
								//TODO handle the exception
							};
							uni.request({
								url: helper.baseUrl+ "/mylike/remove",
								data: {
									username: this.wusername,
									bookname: bookname_1
								},
								method: "POST",
								success: (res) => {
									uni.showToast({
										icon: "success",
										title: res.data.desc
									});
									setTimeout(function() {
										// console.log('start pulldown');
									}, 1000);
									//uni.startPullDownRefresh();
									uni.startPullDownRefresh({
										success: function(res) {
											// console.log(res); //success 返回参数说明
										}
									}); //这里表示当进入页面的时候就开始执行下拉刷新动画
									
								},
								fail: (res) => {
									uni.showToast({
										icon:"none",
										title:"网络连接出错"
									})
								}
							});
						} else if (res.cancel == true) {

						}
					},
				})

			},
			goaddbook() {
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
				} catch (e) {
					//TODO handle the exception
				};
				if (data == "") {
					uni.showModal({
						title: '提示',
						content: '未登录,是否进行登录',
						success: function(res) {
							if (res.confirm == true) {
								uni.navigateTo({
								    url: "../login/login",
									animationType:"zoom-out",
									animationDuration:500
								});
							} else if (res.cancel == true) {
								uni.showToast({
									icon: "none",
									title: "未登录"
								})
							}
						}
					});
				} else {
					uni.showModal({
						title: '提示',
						content: '已登录,是否前往找书',
						success: function(res) {
							if (res.confirm == true) {
								uni.reLaunch({
									url: "../index/index"
								})
							} else if (res.cancel == true) {
								uni.showToast({
									icon: "none",
									title: "操作取消"
								})
							}
						}
					});
				}
			},
			getlike() {
				var like_book = "";
				var data = "";
				var lenbook = 0
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					if (data.walimit == 9) {
						this.wusername = data.wusername;
					} else if (data.walimit == 99) {
						this.wusername = data.wusername;
					} else if(data.walimit == 999){
						this.wusername = data.wadminname;
					}
				} catch (e) {
					//TODO handle the exception
				};
				if (data == "") {

				} else {
					uni.request({
						url: helper.baseUrl + "/my/mylike",
						data: {
							username: this.wusername
						},
						method: "POST",
						success: (res) => {
							like_book = res.data.like;
							this.likebook = like_book;
						}
					});
				}

			},
			getbookimg() {
				var data = [{
					url: "../../static/img/book_add.png",
					name: "添加图书"
				}];
				this.book_add_img = data;
			},
			gotodetail(id, name) {
				var bookname_1 = name;
				var data = "";
				uni.showModal({
					title: '提示',
					content: '前往阅读此书?',
					success: function(res) {
						if (res.confirm == true) {
							uni.navigateTo({
								url: `../bookdata/bookdata-goods?id=${id}`,
								animationType:"zoom-fade-out",
								animationDuration:500
							})
						} else if (res.cancel == true) {

						}
					}
				});
			},

		}
	}
</script>

<style>
	.book_read_top {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
	}

	.book_read_rest {
		width: 100%;
		border-top: 0.5upx solid #e7e7e7;
		display: flex;
		flex-wrap: wrap;
		padding-top: 10upx;
		padding-bottom: 10upx;
	}

	.book-img-item {
		width: 33%;
		padding: 10upx 25upx;
	}

	.book-img-item image {
		width: 200upx;
		height: 320upx;
		float: left;
	}

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
