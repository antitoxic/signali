## Using webpack for frontend
Options for handling images and fonts:

 1. *(I hope we don't have to do this)* [File loader](https://github.com/webpack/file-loader) or [URL loader](https://github.com/webpack/url-loader) to move images from source directory to build directory.
   > to copy a file from your context directory into the output directory retaining the full directory structure, you might use `?name=name=[path][name].[ext]`.
   Both loader's pages linked above include examples
 1. sass loader
  - https://github.com/ddelbondio/ruby-sass-loader
  - https://github.com/webpack/css-loader/issues/34
  - https://github.com/webpack/css-loader