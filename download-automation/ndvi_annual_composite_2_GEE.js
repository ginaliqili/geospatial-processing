// Function to cloud mask Landsats 5-7
var maskL57SR = function(image) {
  var qa = image.select('pixel_qa');
  // Second bit must be zero, meaning none to low cloud confidence.
  var mask1 = qa.bitwiseAnd(ee.Number(2).pow(7).int()).eq(0).and(
      qa.bitwiseAnd(ee.Number(2).pow(3).int()).lte(0)); // cloud shadow
  // This gets rid of irritating fixed-pattern noise at the edge of the images.
  var mask2 = image.select('B.*').gt(0).reduce('min');
  return image.updateMask(mask1.and(mask2));
};

// Function to cloud mask Landsat 8.
var maskL8SR = function(image) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively.
  var cloudShadowBitMask = ee.Number(2).pow(3).int();
  var cloudsBitMask = ee.Number(2).pow(5).int();
  // Get the QA band.
  var qa = image.select('pixel_qa');
  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).and(
            qa.bitwiseAnd(cloudsBitMask).eq(0));
  return image.updateMask(mask);
};

// NDVI functions
var ndviFunction = function(image) {
  image = ee.Image(image)
  return image.addBands(image.expression(
    '(B4-B3) / (B4 + B3)', {
      B4: image.select(['B4']),
      B3: image.select(['B3'])}).rename('NDVI').clamp(-1, 1)).float();
};

var ndviFunctionL8 = function(image) {
  image = ee.Image(image)
  return image.addBands(image.expression(
    '(B5-B4) / (B5 + B4)', {
      B5: image.select(['B5']),
      B4: image.select(['B4'])}).rename('NDVI').clamp(-1, 1)).float();
};



///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////


// Define a region roughly covering the continental US.
var region = ee.Geometry.Rectangle(-127.18, 19.39, -62.75, 51.29);


var lst7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR')
    .filterDate('2013-01-01', '2013-12-31')
    .filterBounds(region)
    .map(maskL57SR);
    
var lst8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .filterDate('2014-01-01', '2014-12-31')
    .filterBounds(region)
    .map(maskL8SR);
    

    
//map the ndvi function
var ndvi = lst7.map(ndviFunction)
var ndviL8 = lst8.map(ndviFunctionL8)

//reduce the ndvi stack
var ndvi_reduced = ndvi.max().clip(region)
var ndvi_reduced_l8 = ndviL8.max().clip(region)

print('reduced ndvi', ndvi_reduced_l8.select('NDVI'));

Map.addLayer(ndvi_reduced_l8.select('NDVI'), {}, 'ndvi reduced');

// Load Census tracts
//var tracts = ee.FeatureCollection('users/gili4697/us_contiguous_census_tracts');
var tracts = ee.FeatureCollection('users/gili4697/us_contiguous_census_tracts');

// Compute NDVI mean of the tracts
var tractMeansFeatures = ndvi_reduced_l8.select('NDVI').reduceRegions({
  collection: tracts,
  reducer: ee.Reducer.mean(),
  scale: 30,
});

print(tractMeansFeatures)

Export.table.toDrive({
  collection: tractMeansFeatures,
  description: 'us_tracts_ndvi_2014',
  fileFormat: 'SHP'
})

// Export the image, specifying scale and region.
/*Export.image.toDrive({
  image: ndvi_reduced.select('NDVI'),
  description: 'L72012NDVI',
  scale: 30,
  region: region.bounds(),
  maxPixels:1e11,
  skipEmptyTiles: true
});*/
// Export the image, specifying scale and region.
/*Export.image.toDrive({
  image: ndvi_reduced.select('NDVI'),
  description: 'L72012NDVI',
  scale: 30,
  region: region.bounds(),
  maxPixels:1e11,
  skipEmptyTiles: true
});*/