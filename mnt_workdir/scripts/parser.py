import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Runs automatic mask generation on an input image or directory of images, "
            "and outputs masks as either PNGs or COCO-style RLEs. Requires open-cv, "
            "as well as pycocotools if saving in RLE format."
            )
    )

    parser.add_argument(
        "--input",
        type=str,
        default='/mnt/imgs/nobiru.jpg',
        help="Path to either a single input image or folder of images.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default='/mnt/output/',
        help=(
            "Path to the directory where masks will be output. Output will be either a folder "
            "of PNGs per image or a single json with COCO-style masks."
        ),
    )

    parser.add_argument(
        "--model-type",
        type=str,
        default='default',
        help="The type of model to load, in ['default', 'vit_h', 'vit_l', 'vit_b']",
    )

    parser.add_argument(
        "--checkpoint",
        type=str,
        default="/mnt/ckpt/sam_vit_l_0b3195.pth",
        help="The path to the SAM checkpoint to use for mask generation.",
    )

    parser.add_argument("--device", type=str, default="cuda", help="The device to run generation on.")

    parser.add_argument(
        "--convert-to-rle",
        action="store_true",
        help=(
            "Save masks as COCO RLEs in a single json instead of as a folder of PNGs. "
            "Requires pycocotools."
        ),
    )

    amg_settings = parser.add_argument_group("AMG Settings")

    amg_settings.add_argument(
        "--points-per-side",
        type=int,
        default=None,
        help="Generate masks by sampling a grid over the image with this many points to a side.",
    )

    amg_settings.add_argument(
        "--points-per-batch",
        type=int,
        default=None,
        help="How many input points to process simultaneously in one batch.",
    )

    amg_settings.add_argument(
        "--pred-iou-thresh",
        type=float,
        default=None,
        help="Exclude masks with a predicted score from the model that is lower than this threshold.",
    )

    amg_settings.add_argument(
        "--stability-score-thresh",
        type=float,
        default=None,
        help="Exclude masks with a stability score lower than this threshold.",
    )

    amg_settings.add_argument(
        "--stability-score-offset",
        type=float,
        default=None,
        help="Larger values perturb the mask more when measuring stability score.",
    )

    amg_settings.add_argument(
        "--box-nms-thresh",
        type=float,
        default=None,
        help="The overlap threshold for excluding a duplicate mask.",
    )

    amg_settings.add_argument(
        "--crop-n-layers",
        type=int,
        default=None,
        help=(
            "If >0, mask generation is run on smaller crops of the image to generate more masks. "
            "The value sets how many different scales to crop at."
        ),
    )

    amg_settings.add_argument(
        "--crop-nms-thresh",
        type=float,
        default=None,
        help="The overlap threshold for excluding duplicate masks across different crops.",
    )

    amg_settings.add_argument(
        "--crop-overlap-ratio",
        type=int,
        default=None,
        help="Larger numbers mean image crops will overlap more.",
    )

    amg_settings.add_argument(
        "--crop-n-points-downscale-factor",
        type=int,
        default=None,
        help="The number of points-per-side in each layer of crop is reduced by this factor.",
    )

    amg_settings.add_argument(
        "--min-mask-region-area",
        type=int,
        default=None,
        help=(
            "Disconnected mask regions or holes with area smaller than this value "
            "in pixels are removed by postprocessing."
        ),
    )
    args = parser.parse_args()
    return args

def get_amg_kwargs(args):
    amg_kwargs = {
        "points_per_side": args.points_per_side,
        "points_per_batch": args.points_per_batch,
        "pred_iou_thresh": args.pred_iou_thresh,
        "stability_score_thresh": args.stability_score_thresh,
        "stability_score_offset": args.stability_score_offset,
        "box_nms_thresh": args.box_nms_thresh,
        "crop_n_layers": args.crop_n_layers,
        "crop_nms_thresh": args.crop_nms_thresh,
        "crop_overlap_ratio": args.crop_overlap_ratio,
        "crop_n_points_downscale_factor": args.crop_n_points_downscale_factor,
        "min_mask_region_area": args.min_mask_region_area,
    }
    amg_kwargs = {k: v for k, v in amg_kwargs.items() if v is not None}
    return amg_kwargs

