// Define a region roughly covering the continental US.
var region = ee.Geometry.Rectangle(-127.18, 19.39, -62.75, 51.29);

//Import Landsat Image
//var L82013NDVI = ee.ImageCollection('LANDSAT/LC08/C01/T1_ANNUAL_NDVI')
var L72013NDVI = ee.ImageCollection('LANDSAT/LE07/C01/T1_ANNUAL_NDVI')
  .filterDate('2013-01-01', '2013-12-31')
  .filterBounds(region);

print('L72013NDVI', L72013NDVI);

Map.addLayer(L72013NDVI.mean().clip(region));

// Export the image, specifying scale and region.
Export.image.toDrive({
  image: L72013NDVI.mean().clip(region),
  description: 'L72013NDVI',
  scale: 30,
  region: region.bounds(),
  maxPixels:1e11,
  skipEmptyTiles: true
});