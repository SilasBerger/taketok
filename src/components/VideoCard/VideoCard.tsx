import "./VideoCard.css";
import {VideoFullInfo} from "../../shared/models";

function VideoCard({videoInfo, onClick}: {videoInfo: VideoFullInfo, onClick: () => void}) {
  return (
    <div class="video-card-container rounded-2xl relative overflow-hidden cursor-pointer shadow-lg" onclick={onClick}>
      <img width="100%" src={`http://127.0.0.1:5000/thumbnail/dev/${videoInfo.video.id}`} />
      <div class="info-drawer
                  absolute bottom-0 z-10
                  flex flex-col justify-end
                  overflow-hidden
                  h-1/4
                  bg-gray-100 bg-opacity-60 backdrop-blur-md
                  w-full transition-all">
        <div class="stretch block p-4 overflow-hidden">{videoInfo.video.transcript}</div>
        <div class="text-right py-1 px-4 text-sm">
          by <span class="text-blue-500 font-bold">@{videoInfo.author.unique_id}</span>
        </div>
      </div>
    </div>
  );
}

export default VideoCard;