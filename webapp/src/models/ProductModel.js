class ProductModel {
  constructor() {
    this.id = null;
    this.ref = null;
    this.fetched = null;
    this.name = null;
    this.category_ref = null;
    this.description = null;
    this.in_stock = null;
    this.price_usd = null;
    this.price_zwg = null;
    this.last_updated = null;
    this.image_url = null;
  }

  setId(id) {
    this.id = id;
    return this;
  }

  setRef(ref) {
    this.ref = ref;
    return this;
  }

  setFetched(fetched) {
    this.fetched = fetched;
    return this;
  }

  setName(name) {
    this.name = name;
    return this;
  }

  setCategoryRef(category_ref) {
    this.category_ref = category_ref;
    return this;
  }

  setDescription(description) {
    this.description = description;
    return this;
  }

  setInStock(in_stock) {
    this.in_stock = in_stock;
    return this;
  }

  setPriceUsd(price_usd) {
    this.price_usd = price_usd;
    return this;
  }

  setPriceZwg(price_zwg) {
    this.price_zwg = price_zwg;
    return this;
  }

  setLastUpdated(last_updated) {
    this.last_updated = last_updated;
    return this;
  }

  setImageUrl(image_url) {
    this.image_url = image_url;
    return this;
  }

  // Optional: populate from a data object
  fromObject(data = {}) {
    return this
      .setId(data.id)
      .setRef(data.ref)
      .setFetched(data.fetched)
      .setName(data.name)
      .setCategoryRef(data.category_ref)
      .setDescription(data.description)
      .setInStock(data.in_stock)
      .setPriceUsd(data.price_usd)
      .setPriceZwg(data.price_zwg)
      .setLastUpdated(data.last_updated)
      .setImageUrl(data.image_url);
  }

  // Optional: convert instance to plain object
  toJson() {
    return {
      id: this.id,
      ref: this.ref,
      fetched: this.fetched,
      name: this.name,
      category_ref: this.category_ref,
      description: this.description,
      in_stock: this.in_stock,
      price_usd: this.price_usd,
      price_zwg: this.price_zwg,
      last_updated: this.last_updated,
      image_url: this.image_url
    };
  }
}

export default ProductModel;
