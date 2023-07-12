function TikTokVideo({videoId}: {videoId: string}) {
  return (
    <video
      controls={true}
      autoplay={true}
      playsinline
      class="h-full">
      <source src={`http://127.0.0.1:5000/video/dev/${videoId}`} type="video/mp4" />
    </video>
  );
}

export default TikTokVideo;