$(document).ready(function () {
    function formatStr() {
        for (let key in data_json) {
            tx = document.querySelectorAll(`#${key} .my-text-wrap`);
            const lineNum = 3; // 设置行数
            for (let i = 0; i < tx.length; i++) {
                let ele = tx[i];
                let item = data_json[key][i];
                let text = `${item["starring"]} / ${item["film_producer"]} / ${item["film_duration"]} / ${item["film_type"]} / ${item["film_language"]}`;
                let totalTextLen = text.length;
                // for (let i = 0; i < text.length; i++) {
                //     if (text[i] == ' ' || text[i] == '/'|| text[i] == '·')
                //         continue;
                //     totalTextLen++;
                // }
                // console.log('totalTextLen:', totalTextLen)
                let baseWidth = window.getComputedStyle(ele).width; // 获取容器的宽度
                // console.log('baseWidth', baseWidth)
                let baseFontSize = window.getComputedStyle(ele).fontSize; // 获取容器的fontSize
                // console.log('baseFontSize', baseFontSize)
                let lineWidth = +baseWidth.slice(0, -2); // 容器宽度去掉px，得到数字类型

                // 所计算的strNum为元素内部一行可容纳的字数(不区分中英文)
                let strNum = Math.floor(lineWidth / +baseFontSize.slice(0, -2));
                // console.log('strNum', strNum)
                let content = '';
                // 多行可容纳总字数
                let totalStrNum = Math.floor(strNum * lineNum);
                // 判断多行可容纳的文字数量是否大于实际文字长度
                let lastIndex = totalStrNum - totalTextLen;
                // 如果实际文字数量超出了多行可容纳的最大数量
                if (totalTextLen > totalStrNum) {
                    // 就把多余的文字数量及前三个去掉
                    // 把去掉多余的文字去掉后，再加上 ...
                    content = text.slice(0, lastIndex - 3).concat('...');
                } else {
                    content = text;
                }
                ele.innerHTML = content;
            }
        }
    }
    data_json = JSON.parse(data_json);
    console.log(data_json);
    for (let key in data_json) {
        let rank = data_json[key];
        let name = "";
        if (key == "short_comment_num_rank")
            name = "评论数";
        else if (key == "question_num_rank")
            name = "提问数";
        else if (key == "score_rank")
            name = "评分";
        else if (key == "topic_num_rank")
            name = "话题数";
        $(`#${key}`).append(`<div class="col-12 h3 mt-3">电影${name}排行榜</div>`);
        $(`#${key}`).append(`<ul class="list-unstyled">`);
        for (let i = 0; i < rank.length; i++) {
            item = rank[i];
            $(`#${key}>ul`).append(
                `
    <li class="my-1">
        <div class="row">
            <div class="col-2">
                <a href="/film/introduction?film_id=${item["film_id"]}" class="text-muted text-decoration-none">
                    <img src="${item["film_poster"]}" class="img-fluid rounded" alt="${item["film_name"]}">
                </a>
            </div>
            <div class="col-6">
                <a href="/film/introduction?film_id=${item["film_id"]}" class="text-muted text-decoration-none text-truncate">
                    ${item["film_name"]}
                </a>
                <p class="my-text-wrap small mb-1" title="${item["starring"]} / ${item["film_producer"]} / ${item["film_duration"]} / ${item["film_type"]} / ${item["film_language"]}">
                    ${item["starring"]} / ${item["film_producer"]} / ${item["film_duration"]} / ${item["film_type"]} / ${item["film_language"]}
                </p>
                <div class="small">${name} ${item[key.slice(0, -5)]}</div>
            </div>
        </div>
    </li>
    `
            );
        }
    }
    //     question_num_rank = data_json["question_num_rank"];
    //     $("#question_num_rank").append(`<div class="col-12 h3 mt-3">电影提问数排行榜</div>`);
    //     $("#question_num_rank").append(`<ul class="list-unstyled">`);
    //     for (let i = 0; i < question_num_rank.length; i++) {
    //         item = question_num_rank[i];
    //         $("#question_num_rank>ul").append(
    //             `
    // <li class="my-1">
    //     <div class="row">
    //         <div class="col-2">
    //             <a href="/film/introduction?film_id=${item["film_id"]}" class="text-muted text-decoration-none">
    //                 <img src="${item["film_poster"]}" class="img-fluid rounded" alt="${item["film_name"]}">
    //             </a>
    //         </div>
    //         <div class="col-6">
    //             <a href="/film/introduction?film_id=${item["film_id"]}" class="text-muted text-decoration-none text-truncate">
    //                 ${item["film_name"]}
    //             </a>
    //             <p class="my-text-wrap small mb-1">${item["starring"]} / ${item["film_producer"]} / ${item["film_duration"]} / ${item["film_type"]} / ${item["film_language"]}</p>
    //             <div class="small">提问数 ${item["question_num"]}</div>
    //         </div>
    //     </div>
    // </li>
    // `
    //         );
    //     }
    formatStr();
    window.onresize = () => {
        formatStr();
    };
})
